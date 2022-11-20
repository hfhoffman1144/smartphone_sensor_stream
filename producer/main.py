import json
from fastapi import FastAPI
from pydantic import BaseModel, validator
from typing import List, Dict
import asyncio
from aiokafka import AIOKafkaProducer
from datetime import datetime

TOPIC_NAME = "phone-stream"
KAFKA_SERVER = "localhost:9093"

app = FastAPI(title='Phone Stream Producer')

loop = asyncio.get_event_loop()

producer = AIOKafkaProducer(
    loop=loop, client_id='Phone Stream Producer', bootstrap_servers=KAFKA_SERVER
)

@app.on_event("startup")
async def startup_event():
    await producer.start()


@app.on_event("shutdown")
async def shutdown_event():
    await producer.stop()

class SensorReading(BaseModel):
    messageId: int
    sessionId: str
    deviceId: str
    payload: List[Dict]

class SensorResponse(BaseModel):
    messageId: str
    sessionId: str
    deviceId: str
    timestamp: str = ""

    @validator("timestamp", pre=True, always=True)
    def set_datetime_utcnow(cls, v):
        return str(datetime.utcnow())

@app.post("/phone-producer/")
async def kafka_produce(data: SensorReading):

    """TODO"""

    await producer.send(TOPIC_NAME, json.dumps(data.dict()).encode("ascii"))

    response = SensorResponse(
        messageId=data.messageId,
        sessionId=data.sessionId,
        deviceId=data.deviceId
    )

    return 200




