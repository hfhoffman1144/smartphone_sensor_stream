import json
from fastapi import FastAPI
import asyncio
from aiokafka import AIOKafkaProducer
from schemas.sensors import SensorReading, SensorResponse
from core.config import app_config
from loguru import logger

app = FastAPI(title=app_config.PROJECT_NAME)

loop = asyncio.get_event_loop()

producer = AIOKafkaProducer(
    loop=loop, client_id=app_config.PROJECT_NAME, bootstrap_servers=app_config.KAFKA_SERVER
)

@app.on_event("startup")
async def startup_event():
    await producer.start()

@app.on_event("shutdown")
async def shutdown_event():
    await producer.stop()

@app.post("/phone-producer/")
async def kafka_produce(data: SensorReading):

    """
    Produce a message containing readings from a smartphone sensor.

    Parameters
    ----------
    data : SensorReading
        The request body containing sensor readings and metadata.

    Returns
    -------
    response : SensorResponse
        The response body corresponding to the processed sensor readings
        from the request.
    """

    await producer.send(app_config.TOPIC_NAME, json.dumps(data.dict()).encode("ascii"))

    response = SensorResponse(
        messageId=data.messageId,
        sessionId=data.sessionId,
        deviceId=data.deviceId
    )

    logger.info(response)

    return response




