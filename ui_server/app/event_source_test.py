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


logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()
origins = [
   f"http://localhost:5001",
   f"http://127.0.0.1:5001",
   f"http://0.0.0.0:5001"
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

@app.get("/test", response_class=HTMLResponse)
async def index(request: Request) -> templates.TemplateResponse:
    return templates.TemplateResponse("event_source_test.html", {"request": request})

@app.get('/sse1')
async def sse_test1(request: Request):
    async def event_generator():
        while True:
           
            if await request.is_disconnected():
                logger.info('client disconnected')
                break
            logger.info('sending message 1')
            yield {
                    "event": "new_message",
                    "id": "message_id",
                    "retry":1500000,
                    "data": 'message'
            }

            await asyncio.sleep(1) #  This contributes to the latency between actual reading and dashboard display?

    return EventSourceResponse(event_generator())

@app.get('/sse2')
async def sse_test2(request: Request):
    async def event_generator():
        while True:
           
            if await request.is_disconnected():
                logger.info('client disconnected')
                break
            logger.info('sending message 2')
            yield {
                    "event": "new_message",
                    "id": "message_id",
                    "retry":1500000,
                    "data": 'message2'
            }

            await asyncio.sleep(3) #  This contributes to the latency between actual reading and dashboard display?

    return EventSourceResponse(event_generator())