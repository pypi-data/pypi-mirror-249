package io.dyff.kafka.streams

import java.io.File
import java.nio.charset.StandardCharsets
import java.time.Duration
import java.util.Base64
import java.util.Properties

import scala.util.{Properties => ScalaProperties}

import org.apache.commons.io.FileUtils
import org.apache.kafka.streams.KafkaStreams
import org.apache.kafka.streams.KeyValue
import org.apache.kafka.streams.StreamsConfig
import org.apache.kafka.streams.Topology
import org.apache.kafka.streams.scala.StreamsBuilder
import org.apache.kafka.streams.scala.kstream._

import _root_.io.dyff.kafka.streams.implicits.JsonMessageImplicits
import _root_.io.dyff.kafka.streams.implicits.MessageImplicits
import _root_.io.dyff.kafka.streams.implicits.MsgpackMessageImplicits


/**
 * Represents a Kubernetes `ConfigMap` resource.
 */
trait ConfigMap {
  /**
   * Return a value in the `data` section, applying an implicit conversion.
   */
  def data[T](key: String)(implicit conversion: String => T): Option[T]

  /**
   * Return a value in the `binaryData` section, applying an implicit conversion.
   */
  def binaryData[T](key: String)(implicit conversion: Array[Byte] => T): Option[T]
}


/**
 * A `ConfigMap` where the values have been mounted as files in `/etc/config`.
 */
class MountedConfigMap extends ConfigMap {
  val configDir: File = new File("/etc/config")

  val configMap: Map[String, String] = {
    configDir.listFiles.map(f => f.getName() -> FileUtils.readFileToString(f, StandardCharsets.UTF_8)).toMap
  }

  def data[T](key: String)(implicit conversion: String => T): Option[T] = {
    configMap.get(key).map(v => v: T)
  }

  def binaryData[T](key: String)(implicit conversion: Array[Byte] => T): Option[T] = {
    configMap.get(key).map(v => Base64.getDecoder().decode(v): T)
  }
}


/**
 * A `ConfigMap` where the values have been injected as environment variables
 * using the `envFrom` option.
 */
class EnvironmentVariableConfigMap extends ConfigMap {
  def data[T](key: String)(implicit conversion: String => T): Option[T] = {
    ScalaProperties.envOrNone(key).map(v => v: T)
  }

  def binaryData[T](key: String)(implicit conversion: Array[Byte] => T): Option[T] = {
    ScalaProperties.envOrNone(key).map(v => Base64.getDecoder().decode(v): T)
  }
}


/**
 * Aggregates workflow events into the materialized current state of
 * each entity in the workflow.
 *
 * The following environment variables are used for configuration:
 *
 * <table>
 *   <tr>
 *     <td>DYFF_KAFKA__TOPICS__WORKFLOWS_EVENTS</td>
 *     <td>The name of the workflows events topic. The app consumes from this topic.</td>
 *   </tr>
 *   <tr>
 *     <td>DYFF_KAFKA__TOPICS__WORKFLOWS_STATE</td>
 *     <td>The name of the workflows state topic. The app produces to this topic.</td>
 *   </tr>
 *   <tr>
 *     <td>DYFF_KAFKA__CONFIG__BOOTSTRAP_SERVERS</td>
 *     <td>The Kafka `bootstrap.servers` property.</td>
 *   </tr>
 *   <tr>
 *     <td>DYFF_KAFKA__STREAMS__APPLICATION_ID</td>
 *     <td>The Kafka Streams `application.id` property.</td>
 *   </tr>
 *   <tr>
 *     <td>DYFF_KAFKA__STREAMS__STATE_DIR</td>
 *     <td>The Kafka Streams `state.dir` property.</td>
 *   </tr>
 * </table>
 *
 * @constructor Create a topology builder with the specified config options.
 * @param configMap A [[io.dyff.kafka.streams.ConfigMap]] mapping environment variables to values.
 */
abstract class WorkflowsAggregatorTopologyBuilder(val configMap: ConfigMap) extends MessageImplicits {
  val eventsTopicName: String = configMap.data("DYFF_KAFKA__TOPICS__WORKFLOWS_EVENTS").get
  val stateTopicName: String = configMap.data("DYFF_KAFKA__TOPICS__WORKFLOWS_STATE").get
  val stateStoreName: String = stateTopicName

  private def mergeValues(base: Option[ujson.Value], update: Option[ujson.Value]): ujson.Value = {
    (base, update) match {
      // Value exists in both inputs
      case (Some(b), Some(u)) => (b.objOpt, u.objOpt) match {
        // If both values are Objects, merge them recursively
        case (Some(x), Some(y)) => mergeObj(x, y)
        // Otherwise, take the 'update' value
        case _ => u
      }
      // Invariant: Never both None because of how mergeObj is implemented
      case _ => (update orElse base).get
    }
  }

  private def mergeObj(base: ujson.Obj, update: ujson.Obj): ujson.Obj = {
    // Create a new Object by merging the (k -> v) pairs in both inputs
    (base.obj.keySet ++ update.obj.keySet).map(
      key => key -> mergeValues(base.obj.get(key), update.obj.get(key))
    )
  }

  /**
   * Construct the Kafka Streams processing Topology.
   */
  def buildTopology(): Topology = {
    import org.apache.kafka.streams.scala.serialization.Serdes._
    import org.apache.kafka.streams.scala.ImplicitConversions._

    val builder: StreamsBuilder = new StreamsBuilder()
    val entityEventsStream = builder.stream[String, ujson.Obj](eventsTopicName)
    val entityStateTable = entityEventsStream
      .groupByKey
      // Overwrite the fields that changed
      .aggregate[ujson.Obj](ujson.Obj())(
        (key: String, event: ujson.Obj, state: ujson.Obj) => {
          mergeObj(state, event)
        }
      )(Materialized.as(stateStoreName))
    entityStateTable.toStream.to(stateTopicName)
    builder.build()
  }

  def kafkaProperties(): Properties = {
    // This should always be exactly_once_v2; raise an error if user tries to
    // set it to something else.
    configMap.data[String]("DYFF_KAFKA__STREAMS__PROCESSING_GUARANTEE").map(v => {
      if (v != StreamsConfig.EXACTLY_ONCE_V2) {
        throw new IllegalArgumentException(
          s"DYFF_KAFKA__STREAMS__PROCESSING_GUARANTEE must be ${StreamsConfig.EXACTLY_ONCE_V2}")
      }
    })

    val p = new Properties()
    p.put(
      StreamsConfig.PROCESSING_GUARANTEE_CONFIG,
      StreamsConfig.EXACTLY_ONCE_V2
    )
    p.put(
      StreamsConfig.BOOTSTRAP_SERVERS_CONFIG,
      configMap.data[String]("DYFF_KAFKA__CONFIG__BOOTSTRAP_SERVERS").get
    )
    p.put(
      StreamsConfig.APPLICATION_ID_CONFIG,
      configMap.data[String]("DYFF_KAFKA__STREAMS__APPLICATION_ID").get
    )
    p.put(
      StreamsConfig.STATE_DIR_CONFIG,
      configMap.data[String]("DYFF_KAFKA__STREAMS__STATE_DIR").get
    )
    p.put(
      StreamsConfig.DEFAULT_DESERIALIZATION_EXCEPTION_HANDLER_CLASS_CONFIG,
      "org.apache.kafka.streams.errors.LogAndContinueExceptionHandler"
    )
    // TODO: Probably at least 2 threads, depending on k8s resource config
    // p.put(StreamsConfig.NUM_STREAM_THREADS_CONFIG, 2)
    p
  }
}

/**
 * EntityStateApp using JSON string encoding for messages.
 */
class WorkflowsAggregatorTopologyBuilderWithJson(configMap: ConfigMap)
  extends WorkflowsAggregatorTopologyBuilder(configMap)
  with JsonMessageImplicits
{ }

/**
 * EntityStateApp using Msgpack encoding for messages.
 */
class WorkflowsAggregatorTopologyBuilderWithMsgpack(configMap: ConfigMap)
  extends WorkflowsAggregatorTopologyBuilder(configMap)
  with MsgpackMessageImplicits
{ }


object WorkflowsAggregatorApp extends App {
  val configMap: ConfigMap = new EnvironmentVariableConfigMap()
  val builder = new WorkflowsAggregatorTopologyBuilderWithJson(configMap)

  // TODO: Kubernetes bootstrap server
  // TODO: PVC mount point for persistence
  val config: Properties = builder.kafkaProperties()
  val topology = builder.buildTopology()

  val streams: KafkaStreams = new KafkaStreams(topology, config)
  streams.start()

  sys.ShutdownHookThread {
    streams.close(Duration.ofSeconds(10))
  }
}
