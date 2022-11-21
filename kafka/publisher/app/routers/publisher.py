import json

from app.core.gateways.kafka import Kafka
from app.core.models.message import Message
from app.dependencies.kafka import get_kafka_instance

from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("")
async def send(data: Message, server: Kafka = Depends(get_kafka_instance)):
    try:
        data = data.dict()
        await server.aioproducer.send_and_wait(data.get("topic"), json.dumps(data).encode("ascii"))
    except Exception as e:
        await server.aioproducer.stop()
        raise e
    return 'Message sent successfully'
