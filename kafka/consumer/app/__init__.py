import os
from json import loads

from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from app.cosmos_factory import CosmosFactory


def main():
    print("Start Kafka Consumer...")
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
            print("%s:%d:%d: value=%s" % (message.topic, message.partition,
                                          message.offset, message.value))
            cosmos_container = CosmosFactory.get_container(message.topic)
            cosmos_container.upsert_item(body=message.value)

    except NoBrokersAvailable as e:
        print("Unable to find a broker: {}".format(e))
