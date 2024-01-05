package io.dyff.kafka.streams.implicits

import java.nio.charset.StandardCharsets.UTF_8

import org.apache.kafka.common.serialization.Deserializer
import org.apache.kafka.common.serialization.Serde
import org.apache.kafka.common.serialization.Serializer
import upickle.default._

/**
 * Mixin to define implicit conversions for Kafka (de)serialization.
 */
trait MessageImplicits {
  outer =>

  implicit def serializer[T: Writer]: Serializer[T]

  implicit def deserializer[T: Reader]: Deserializer[T]

  implicit def serde[T: ReadWriter]: Serde[T] = {
    new Serde[T] {
      override def serializer(): Serializer[T] = outer.serializer[T]
      override def deserializer(): Deserializer[T] = outer.deserializer[T]
    }
  }
}

object MessageImplicits { }


/**
 * Mixin to define implicit conversions needed for JSON messages.
 *
 * This is copied near-verbatim from the `kafka-serde-scala` package, which
 * is licensed under the Apache 2.0 license.
 * @see <a href="https://github.com/azhur/kafka-serde-scala/blob/main/kafka-serde-upickle/src/main/scala/io/github/azhur/kafka/serde/UpickleSupport.scala"/>
 */
trait JsonMessageImplicits extends MessageImplicits {
  implicit def serializer[T: Writer]: Serializer[T] = {
    new Serializer[T] {
      override def serialize(topic: String, data: T): Array[Byte] = {
        write(data).getBytes(UTF_8)
      }
    }
  }

  implicit def deserializer[T: Reader]: Deserializer[T] = {
    new Deserializer[T] {
      override def deserialize(topic: String, data: Array[Byte]): T = {
        read[T](new String(data, UTF_8))
      }
    }
  }
}

object JsonMessageImplicits extends JsonMessageImplicits


/**
 * Mixin to define implicit conversions needed for Msgpack messages.
 */
trait MsgpackMessageImplicits extends MessageImplicits {
  implicit def serializer[T: Writer]: Serializer[T] = {
    new Serializer[T] {
      override def serialize(topic: String, data: T): Array[Byte] = {
        writeBinary(data)
      }
    }
  }

  implicit def deserializer[T: Reader]: Deserializer[T] = {
    new Deserializer[T] {
      override def deserialize(topic: String, data: Array[Byte]): T = {
        readBinary[T](data)
      }
    }
  }
}

object MsgpackMessageImplicits extends MsgpackMessageImplicits
