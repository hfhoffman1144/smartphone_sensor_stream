from datetime import datetime
import psycopg2 as pg
import pandas as pd
from io import StringIO
import requests
from models.sensors import SensorName


# Map sensor names from a payload to their corresponding name in the db
DEVICE_TO_DB_SENSOR_NAME = {

    SensorName.ACC.value: 'acc',
    SensorName.GYRO.value: 'gyro',
    SensorName.MAG.value: 'mag'

}

def create_connection(host:str, port:str, user_name:str, password:str, database:str):

    """
    Create a Postgres database connection

    Parameters
    ----------
    host:str
        Database host
    port:str
        Database port
    user_name:str
        Database user name
    password:str
        Database password
    database:str
        Database name

    Returns
    -------
    A psycopg2 connection object
    """

    return pg.connect(user=user_name,
                      password=password,
                      host=host,
                      port=port,
                      database=database,
                      options='-c statement_timeout=300000')

def create_triaxial_table(table_name:str, connection:pg.connect):

    """
    Create a table that can store data from triaxial smartphone sensors

    Parameters
    ----------
    table_name : str
        The name of the table to create
    connection: pg.connection
        A pyscopg2 connection object
    """

    cursor = connection.cursor()
    
    sql = f"""CREATE TABLE IF NOT EXISTS {table_name} (
            device_id TEXT,
            session_id TEXT,
            device_timestamp TEXT,
            recorded_timestamp TEXT,
            sensor_name TEXT,
            x REAL,
            y REAL,
            z REAL)"""

    cursor.execute(sql)
    connection.commit()


def write_sensor_payloads(data:dict, server_url:str, table_name:str):
    
    """
    Write phone sensor data to database tables

    Parameters
    ----------
    data : dict
        The raw request data sent by the phone
    server_url : str
        The URL where sensor data will be written to
    table_name : str
        The name of the table to write to 
    """

    session_id = data['sessionId']
    device_id = data['deviceId']

    # Create an empty dict to store structured sensor from the payload
    structured_payload = {'device_id':[],
                            'session_id':[],
                            'device_timestamp':[],
                            'recorded_timestamp':[],
                            'sensor_name':[],
                            'x':[],
                            'y':[],
                            'z':[]
                            }
    
    for d in data['payload']:

        # Triaxial sensors
        if d.get("name") in DEVICE_TO_DB_SENSOR_NAME.keys():

            structured_payload['device_id'].append(device_id)
            structured_payload['session_id'].append(session_id)
            structured_payload['device_timestamp'].append(str(datetime.fromtimestamp(int(d["time"]) / 1000000000)))
            structured_payload['recorded_timestamp'].append(str(datetime.utcnow()))
            structured_payload['sensor_name'].append(DEVICE_TO_DB_SENSOR_NAME.get(d.get("name")))
            structured_payload['x'].append(d["values"]["x"])
            structured_payload['y'].append(d["values"]["y"])
            structured_payload['z'].append(d["values"]["z"])  

    output = StringIO()
    pd.DataFrame(structured_payload).to_csv(output, sep=',', header=True, index=False)
    output.seek(0)
    contents = output.getvalue()
    csv = {'data': (table_name, contents)}
    response = requests.post(server_url, files=csv)


    