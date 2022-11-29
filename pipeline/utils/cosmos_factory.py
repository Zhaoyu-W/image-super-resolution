import os

from azure.cosmos import CosmosClient, PartitionKey


class TopicNotFoundException(Exception):
    pass


class CosmosFactory:
    _db = None
    _ADOBE_COSMOS_CONTAINER = None
    _PIXABAY_CONTAINER = None
    _PEXELS_CONTAINER = None

    def __new__(cls, db_id):
        if cls._db is None:
            print("Creating CosmosDB Proxy...")

            client = CosmosClient(os.environ["COSMOS_URI"], os.environ["COSMOS_KEY"])
            cls._db = client.create_database_if_not_exists(id=db_id)
        return cls._db

    @classmethod
    def get_container(cls, topic, db_name="original"):
        db = cls(db_name)

        if topic == "adobe":
            if not cls._ADOBE_COSMOS_CONTAINER:
                print("Creating adobe container...")

                cls._ADOBE_COSMOS_CONTAINER = db.create_container_if_not_exists(
                    id=topic,
                    partition_key=PartitionKey(path="/title"),
                    offer_throughput=400
                )
            return cls._ADOBE_COSMOS_CONTAINER
        elif topic == "pixabay":
            if not cls._PIXABAY_CONTAINER:
                print("Creating pixabay container...")

                cls._PIXABAY_CONTAINER = db.create_container_if_not_exists(
                    id=topic,
                    partition_key=PartitionKey(path="/title"),
                    offer_throughput=400
                )
            return cls._PIXABAY_CONTAINER
        elif topic == "pexels":
            if not cls._PEXELS_CONTAINER:
                print("Creating pexels container...")

                cls._PEXELS_CONTAINER = db.create_container_if_not_exists(
                    id=topic,
                    partition_key=PartitionKey(path="/title"),
                    offer_throughput=400
                )
            return cls._PEXELS_CONTAINER
        else:
            raise TopicNotFoundException("Topic not found...")
