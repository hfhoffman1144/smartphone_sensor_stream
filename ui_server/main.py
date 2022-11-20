import asyncio
import json
import logging
import random
import psycopg2 as pg
import sys
from enum import Enum
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Iterator
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from sse_starlette.sse import EventSourceResponse


connection = pg.connect(user="admin",
                            password="quest",
                            host="127.0.0.1",
                            port="8812",
                            database="qdb",
                            options='-c statement_timeout=300000')


class SensorName(Enum):
    
    ACC = 'accelerometeruncalibrated'
    GYRO = 'gyroscopeuncalibrated'

TOPIC_NAME = "phone-stream"
KAFKA_SERVER = "localhost:9093"
STREAM_DELAY = 1

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> templates.TemplateResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/chart-data')
async def message_stream(request: Request):
    def new_messages():
        yield True
    async def event_generator():
        while True:
            # If client was closed the connection
            if await request.is_disconnected():
                break

            # Checks for new messages and return them to client if any
            if new_messages():

                data = pd.read_sql("""with tmp as (select device_id,
                                             recorded_timestamp,
                                              x,
                                              y,
                                              z,
                                              row_number() over(partition by device_id order by
                                                                recorded_timestamp desc) as rn
                                               from acc )

                                        select * from tmp where rn <= 40""", 
                                  connection)

                message_data = {}

                for device_id in data['device_id'].unique():

                    data_device = data[data['device_id']==device_id]

                    message_data[device_id] = {
                                    'time':list(data_device['recorded_timestamp'].astype(str).values),
                                    'x':list(data_device['x'].astype(float).values),
                                    'y':list(data_device['y'].astype(float).values),
                                    'z':list(data_device['z'].astype(float).values)
                                }

                message = json.dumps(message_data)
                yield {
                        "event": "new_message",
                        "id": "message_id",
                        "retry":1500000,
                        "data": message
                }

            await asyncio.sleep(0.25)

    return EventSourceResponse(event_generator())