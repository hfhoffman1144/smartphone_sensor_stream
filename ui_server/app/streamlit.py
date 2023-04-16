import time
import logging
import sys
import asyncio

import pandas as pd
import streamlit as st
import plotly.express as px


from core.config import app_config
from db.data_api import create_connection, get_recent_triaxial_data, DEVICE_TO_DB_SENSOR_NAME
from models.sensors import SensorName

from seed.devices import DEVICE_MAPPING

CONNECTION = create_connection(app_config.DB_HOST,
                               app_config.DB_PORT,
                               app_config.DB_USER,
                               app_config.DB_PASSWORD,
                               app_config.DB_NAME )

DATA_POINT_LEN = 50

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Real-Time Device Motion Sensor Dashboard",
    page_icon="📱",
    layout="wide",
)

async def data_generator():
        data = get_recent_triaxial_data(connection=CONNECTION, 
                                        table_name=app_config.DB_TRIAXIAL_OFFLOAD_TABLE_NAME,
                                        sensor_name=DEVICE_TO_DB_SENSOR_NAME[SensorName.ACC.value],
                                        sample_rate=app_config.PHONE_SAMPLE_RATE,
                                        num_seconds=1,
                                        max_lookback_seconds=60)
        message_data = {}

        for device_id in data['device_id'].unique():

            data_device = data[data['device_id']==device_id]
            device_alias = DEVICE_MAPPING[device_id]

            message_data[device_alias] = {
                'time':[t[11:] for t in list(data_device['recorded_timestamp'].astype(str).values)],
                'x':list(data_device['x'].astype(float).values)[0],
                'y':list(data_device['y'].astype(float).values)[0],
                'z':list(data_device['z'].astype(float).values)[0]
                }
        return message_data

# dashboard title
st.title("📱Real-Time Device Motion Sensor Dashboard")

charts = dict()
traces = dict()
figs = dict()

# near real-time / live feed simulation
async def main():
    while True:
        try:
            message_data = await data_generator()
            for device in message_data.keys():
                data = message_data[device]
                if device not in charts:
                    trace = pd.DataFrame(columns=["time", "x", "y", "z"])
                    traces[device] = trace
                    charts[device] = st.empty()
                                    
                traces[device] = traces[device].append({
                    "time": data["time"],
                    "x": data['x'],
                    "y": data['y'],
                    "z": data['z']
                }, ignore_index=True)

                if traces[device].shape[0] > DATA_POINT_LEN:
                    traces[device] = traces[device].iloc[traces[device].shape[0]-DATA_POINT_LEN:]
                figs[device] = px.line(traces[device].set_index("time"), title=f"Device: {device}")
                figs[device].update_xaxes(title_text="X-axis Label")
                figs[device].update_yaxes(title_text="Y-axis Label")
                charts[device].plotly_chart(figs[device])
                                
            time.sleep(1)
        except Exception as e:
            logger.error(f'Error: {e}')
            time.sleep(0.01)

asyncio.run(main())