import logging
import os
from json import loads

from kafka import KafkaConsumer


def main():
    try:
        # To consume latest messages and auto-commit offsets
        consumer = KafkaConsumer(
            bootstrap_servers="kafka:29092",
            value_deserializer=lambda x: loads(x.decode("utf-8")),
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )
        consumer.subscribe(os.environ.get("KAFKA_TOPIC_NAME").split(","))

        for message in consumer:
            print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                 message.offset, message.key, message.value))

    except Exception as e:
        logging.info("Connection successful", e)
