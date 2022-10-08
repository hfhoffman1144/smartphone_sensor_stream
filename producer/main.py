import json
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from kafka import KafkaProducer

TOPIC_NAME = "phone-stream"
KAFKA_SERVER = "localhost:9092"

producer = KafkaProducer(
    bootstrap_servers = KAFKA_SERVER,
    api_version = (0, 11, 15)
)

class SensorReading(BaseModel):
    messageId: int
    sessionId: str
    deviceId: str
    payload: List[Dict]

app = FastAPI()


@app.post("/phone-producer/")
async def kafka_produce(data: SensorReading):

    json_payload = json.dumps(data.dict())
    json_payload = str.encode(json_payload)
    producer.send(TOPIC_NAME, json_payload)
    producer.flush()

    return 200




