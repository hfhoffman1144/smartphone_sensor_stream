from typing import List, Dict
from fastapi import FastAPI
from pydantic import BaseModel


class SensorReading(BaseModel):
    messageId: int
    sessionId: str
    deviceId: str
    payload: List[Dict]


app = FastAPI()

@app.post("/data/")
async def consume_reading(data: SensorReading):

    print(data.dict())

    return "success"