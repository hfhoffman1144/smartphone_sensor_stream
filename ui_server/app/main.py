import asyncio
import json
import logging
import sys
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sse_starlette.sse import EventSourceResponse
from core.config import app_config
from db.data_api import create_connection, get_recent_triaxial_data, DEVICE_TO_DB_SENSOR_NAME
from models.sensors import SensorName


CONNECTION = create_connection(app_config.DB_HOST,
                               app_config.DB_PORT,
                               app_config.DB_USER,
                               app_config.DB_PASSWORD,
                               app_config.DB_NAME )

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()
origins = [
   f"http://localhost:{app_config.UI_PORT}",
   f"http://127.0.0.1:{app_config.UI_PORT}",
   f"http://0.0.0.0:{app_config.UI_PORT}"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
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
           
            if await request.is_disconnected():
                break

            if new_messages():

                data = get_recent_triaxial_data(connection=CONNECTION, 
                                                table_name=app_config.DB_TRIAXIAL_OFFLOAD_TABLE_NAME,
                                                sensor_name=DEVICE_TO_DB_SENSOR_NAME[SensorName.ACC.value],
                                                sample_rate=app_config.PHONE_SAMPLE_RATE,
                                                num_seconds=1,
                                                max_lookback_seconds=60)                

                message_data = {}

                for device_id in data['device_id'].unique():

                    data_device = data[data['device_id']==device_id]

                    message_data[device_id] = {
                                    'time':[t[11:] for t in list(data_device['recorded_timestamp'].astype(str).values)],
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

            await asyncio.sleep(0.1)

    return EventSourceResponse(event_generator())