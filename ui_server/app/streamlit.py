import time
import json
import asyncio

import plotly.express as px
import streamlit as st

from core.config import app_config
from db.data_api import create_connection, get_recent_triaxial_data, DEVICE_TO_DB_SENSOR_NAME
from models.sensors import SensorName


CONNECTION = create_connection(app_config.DB_HOST,
                               app_config.DB_PORT,
                               app_config.DB_USER,
                               app_config.DB_PASSWORD,
                               app_config.DB_NAME )


st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
    page_icon="✅",
    layout="wide",
)

async def data_generator():
        # while True:
        data = get_recent_triaxial_data(connection=CONNECTION, 
                                        table_name=app_config.DB_TRIAXIAL_OFFLOAD_TABLE_NAME,
                                        sensor_name=DEVICE_TO_DB_SENSOR_NAME[SensorName.ACC.value],
                                        sample_rate=app_config.PHONE_SAMPLE_RATE,
                                        num_seconds=1,
                                        max_lookback_seconds=60)                

        device_id = list(data['device_id'].unique())[0]
        data_device = data[data['device_id']==device_id]

        data_dict = {
                        'time':[t[11:] for t in list(data_device['recorded_timestamp'].astype(str).values)],
                        'x':list(data_device['x'].astype(float).values)[0],
                        'y':list(data_device['y'].astype(float).values)[0],
                        'z':list(data_device['z'].astype(float).values)[0]
                    }
        return data_dict
# asyncio.run(data_generator())

# dashboard title
st.title("Real-Time / Live Data Science Dashboard")

# top-level filters
# job_filter = st.selectbox("Select the Job", pd.unique(df["job"]))

# creating a single-element container
placeholder = st.empty()

# near real-time / live feed simulation
async def main():
    while True:
        try:
            data_dict = await data_generator()
            with placeholder.container():
                # create three columns
                x_col, y_col, z_col = st.columns(3)
                x, y, z = data_dict['x'], data_dict['y'], data_dict['z']
                print(x,y,z)

                # fill in those three columns with respective metrics or KPIs
                x_col.metric(
                    label="x",
                    value=x,
                )
                
                y_col.metric(
                    label="y",
                    value=y,
                )
                
                z_col.metric(
                    label="z",
                    value=z,
                )
            time.sleep(0.01)
        except Exception:
            time.sleep(0.01)

asyncio.run(main())