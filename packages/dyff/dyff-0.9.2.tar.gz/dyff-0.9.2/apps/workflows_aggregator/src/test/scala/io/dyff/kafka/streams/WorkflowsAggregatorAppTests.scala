package io.dyff.kafka.streams

import java.nio.file.Path
import java.util.Properties
import java.util.Base64
import java.util.UUID

import org.apache.kafka.common.serialization._
import org.apache.kafka.streams.KeyValue
import org.apache.kafka.streams.StreamsConfig
import org.apache.kafka.streams.Topology
import org.apache.kafka.streams.TopologyTestDriver

import org.junit.jupiter.api._
import org.junit.jupiter.api.Assertions._
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.io.TempDir
import org.junit.jupiter.params.ParameterizedTest
import org.junit.jupiter.params.provider.ValueSource
import upickle.default._

import _root_.io.dyff.kafka.streams.ConfigMap
import _root_.io.dyff.kafka.streams.WorkflowsAggregatorTopologyBuilder
import _root_.io.dyff.kafka.streams.implicits.{JsonMessageImplicits, MsgpackMessageImplicits}


class MockConfigMap(val data: Map[String, String], val binaryData: Map[String, String]) extends ConfigMap {
  def data[T](key: String)(implicit conversion: String => T): Option[T] = {
    data.get(key).map(v => v: T)
  }

  def binaryData[T](key: String)(implicit conversion: Array[Byte] => T): Option[T] = {
    binaryData.get(key).map(v => Base64.getDecoder().decode(v): T)
  }
}


class WorkflowsStateAppTests {

  def convertBytesToHex(bytes: Seq[Byte]): String = {
    val sb = new StringBuilder
    for (b <- bytes) {
        sb.append(String.format("%02x", Byte.box(b)))
    }
    sb.toString
  }

  @Test
  def serdesJson(): Unit = {
    import JsonMessageImplicits._
    val original: Map[String, ujson.Value] = Map(
      "foo" -> "bar",
      "answer" -> 42,
      "list" -> List(1, 2, 3)
    )
    println(write(original))

    val serialized =
      implicitly[Serializer[ujson.Value]].serialize("unused topic", original)
    println(s"serialized: ${convertBytesToHex(serialized)}")

    val deserialized: Map[String, ujson.Value] =
      implicitly[Deserializer[ujson.Value]].deserialize("unused topic", serialized).obj.toMap
    println(s"deserialized: $deserialized")

    assertEquals(deserialized, original)
  }

  @Test
  def serdesMsgpack(): Unit = {
    import MsgpackMessageImplicits._
    val original: Map[String, ujson.Value] = Map(
      "foo" -> "bar",
      "answer" -> 42,
      "list" -> List(1, 2, 3)
    )
    println(write(original))

    val serialized =
      implicitly[Serializer[ujson.Value]].serialize("unused topic", original)
    println(s"serialized: ${convertBytesToHex(serialized)}")

    val deserialized: Map[String, ujson.Value] =
      implicitly[Deserializer[ujson.Value]].deserialize("unused topic", serialized).obj.toMap
    println(s"deserialized: $deserialized")

    assertEquals(deserialized, original)
  }

  @ParameterizedTest
  @ValueSource(strings = Array("Json", "Msgpack"))
  def entityEventsToState(serdeFormat: String, @TempDir tempDir: Path): Unit = {
    import org.apache.kafka.streams.scala.serialization.Serdes._

    val configMap = new MockConfigMap(
      data = Map(
        "DYFF_KAFKA__TOPICS__WORKFLOWS_EVENTS" -> "workflows.events",
        "DYFF_KAFKA__TOPICS__WORKFLOWS_STATE" -> "workflows.state",
        // "app.topics.input.events" -> "workflows.events",
        // "app.topics.output.state" -> "workflows.state",

        "DYFF_KAFKA__CONFIG__BOOTSTRAP_SERVERS" -> "dummy config",
        "DYFF_KAFKA__STREAMS__APPLICATION_ID" -> s"workflows-aggregator-app-v0-$serdeFormat",
        "DYFF_KAFKA__STREAMS__STATE_DIR" -> tempDir.toAbsolutePath().toString()
        // "kafka.streams.application.id" -> s"events-to-state-app-v0-$serdeFormat",
        // "kafka.streams.bootstrap.servers" -> "dummy config",
        // "kafka.streams.state.dir" -> tempDir.toAbsolutePath().toString()
      ),
      binaryData = Map()
    )

    val app =
      if (serdeFormat == "Msgpack") {
        new WorkflowsAggregatorTopologyBuilderWithMsgpack(configMap)
      }
      else if (serdeFormat == "Json") {
        new WorkflowsAggregatorTopologyBuilderWithJson(configMap)
      }
      else {
        throw new IllegalArgumentException()
      }

    println(s"$serdeFormat: $tempDir")
    val config: Properties = app.kafkaProperties()
    val topology = app.buildTopology()
    val testDriver = new TopologyTestDriver(topology, config)

    val eventsTopic = testDriver.createInputTopic(
      app.eventsTopicName,
      new StringSerializer,
      app.serializer[ujson.Obj]
    )
    val stateTopic = testDriver.createOutputTopic(
      app.stateTopicName,
      new StringDeserializer,
      app.deserializer[ujson.Obj]
    )
    val kvStore = testDriver.getKeyValueStore[String, ujson.Obj](app.stateStoreName)

    val idA: String = UUID.randomUUID().toString
    val idB: String = UUID.randomUUID().toString
    val dataset: String = UUID.randomUUID.toString

    val createEventA: ujson.Obj = ujson.Obj(
      "_id" -> idA,
      "labels" -> ujson.Obj("name" -> "foobar"),
      "dataset" -> dataset,
      "status" -> "Created"
    )
    eventsTopic.pipeInput(idA, createEventA)
    val createEventAState = stateTopic.readKeyValue()
    println(s"$serdeFormat: $createEventAState")
    assertEquals(createEventA.obj.toMap, createEventAState.value.obj.toMap)
    val createEventAStateStored: ujson.Obj = kvStore.get(idA)
    assertEquals(createEventA.obj.toMap, createEventAStateStored.value.obj.toMap)

    val createEventB: ujson.Obj = Map(
      "_id" -> idB,
      "dataset" -> dataset,
      "status" -> "Created"
    )
    eventsTopic.pipeInput(idB, createEventB)
    val createEventBState = stateTopic.readKeyValue()
    println(s"$serdeFormat: $createEventBState")
    assertEquals(createEventB.obj.toMap, createEventBState.value.obj.toMap)
    val createEventBStateStored: ujson.Obj = kvStore.get(idB)
    assertEquals(createEventB.obj.toMap, createEventBStateStored.value.obj.toMap)

    val statusEventA = Map(
      "status" -> "Admitted"
    )
    eventsTopic.pipeInput(idA, statusEventA)
    val statusEventAState = stateTopic.readKeyValue()
    println(s"$serdeFormat: $statusEventAState")
    val statusEventAStateTruth = createEventA.obj.clone()
    statusEventAStateTruth.put("status", statusEventA.get("status").get)
    assertEquals(statusEventAStateTruth.toMap, statusEventAState.value.obj.toMap)
    val statusEventAStateStored: ujson.Obj = kvStore.get(idA)
    assertEquals(statusEventAStateTruth.toMap, statusEventAStateStored.value.obj.toMap)

    val statusEventB = Map(
      "status" -> "Failed"
    )
    eventsTopic.pipeInput(idB, statusEventB)
    val statusEventBState = stateTopic.readKeyValue()
    println(s"$serdeFormat: $statusEventBState")
    val statusEventBStateTruth = createEventB.obj.clone()
    statusEventBStateTruth.put("status", statusEventB.get("status").get)
    assertEquals(statusEventBStateTruth.toMap, statusEventBState.value.obj.toMap)
    val statusEventBStateStored: ujson.Obj = kvStore.get(idB)
    assertEquals(statusEventBStateTruth.toMap, statusEventBStateStored.value.obj.toMap)

    val labelsEventA = ujson.Obj(
      "labels" -> ujson.Obj("project" -> "jenova")
    )
    eventsTopic.pipeInput(idA, labelsEventA)
    val labelsEventAState = stateTopic.readKeyValue()
    println(s"$serdeFormat: $labelsEventAState")
    val labelsEventAStateTruth = ujson.Obj(
      "_id" -> idA,
      "labels" -> ujson.Obj("name" -> "foobar", "project" -> "jenova"),
      "dataset" -> dataset,
      "status" -> "Admitted"
    )
    assertEquals(labelsEventAStateTruth.obj.toMap, labelsEventAState.value.obj.toMap)
    val labelsEventAStateStored: ujson.Obj = kvStore.get(idA)
    assertEquals(labelsEventAStateTruth.obj.toMap, labelsEventAStateStored.value.obj.toMap)

    val overwriteLabelsEventA = ujson.Obj(
      "labels" -> ujson.Obj("project" -> "crm-114")
    )
    eventsTopic.pipeInput(idA, overwriteLabelsEventA)
    val overwriteLabelsEventAState = stateTopic.readKeyValue()
    println(s"$serdeFormat: $overwriteLabelsEventAState")
    val overwriteLabelsEventAStateTruth = ujson.Obj(
      "_id" -> idA,
      "labels" -> ujson.Obj("name" -> "foobar", "project" -> "crm-114"),
      "dataset" -> dataset,
      "status" -> "Admitted"
    )
    assertEquals(overwriteLabelsEventAStateTruth.obj.toMap, overwriteLabelsEventAState.value.obj.toMap)
    val overwriteLabelsEventAStateStored: ujson.Obj = kvStore.get(idA)
    assertEquals(overwriteLabelsEventAStateTruth.obj.toMap, overwriteLabelsEventAStateStored.value.obj.toMap)

    val labelNoneEventA = ujson.Obj(
      "labels" -> ujson.Obj("project" -> ujson.Null)
    )
    eventsTopic.pipeInput(idA, labelNoneEventA)
    val labelNoneEventAState = stateTopic.readKeyValue()
    println(s"$serdeFormat: $labelNoneEventAState")
    val labelNoneEventAStateTruth = ujson.Obj(
      "_id" -> idA,
      "labels" -> ujson.Obj("name" -> "foobar", "project" -> ujson.Null),
      "dataset" -> dataset,
      "status" -> "Admitted"
    )
    assertEquals(labelNoneEventAStateTruth.obj.toMap, labelNoneEventAState.value.obj.toMap)
    val labelNoneEventAStateStored: ujson.Obj = kvStore.get(idA)
    assertEquals(labelNoneEventAStateTruth.obj.toMap, labelNoneEventAStateStored.value.obj.toMap)

    testDriver.close()
  }
}


object EntityStateTests {

}
