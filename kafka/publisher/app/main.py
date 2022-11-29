import time

from app.core.gateways.kafka import Kafka
from app.dependencies.kafka import get_kafka_instance
from app.routers import publisher

from fastapi import Depends, FastAPI, Request

app = FastAPI(title="Kafka Publisher API")
kafka_server = Kafka(
    port="29092",
    servers="kafka",
)


@app.on_event("startup")
async def startup_event():
    await kafka_server.aioproducer.start()


@app.on_event("shutdown")
async def shutdown_event():
    await kafka_server.aioproducer.stop()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/")
def get_root():
    return {"message': 'API is running..."}


app.include_router(
    publisher.router,
    prefix="/send",
    tags=["send"],
    dependencies=[Depends(get_kafka_instance)],
)
