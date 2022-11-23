from datetime import datetime
from models.sensors import SensorName
import psycopg2 as pg


# Map sensor names from a payload to their corresponding table in the db
SENSOR_TO_TABLE_NAME = {

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
    Create a table that can store data from a triaxial smartphone sensor

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
            x REAL,
            y REAL,
            z REAL)"""

    cursor.execute(sql)
    connection.commit()


def write_sensor_payloads(data:dict, connection:pg.connect):
    
    """
    Write phone sensor data to database tables

    Parameters
    ----------
    data : dict
        The raw request data sent by the phone
    connection: pg.connection
        A pyscopg2 connection object
    """

    session_id = data['sessionId']
    device_id = data['deviceId']
    
    for d in data['payload']:

        # Triaxial sensors
        if d.get("name") in [SensorName.ACC.value, SensorName.GYRO.value, SensorName.MAG.value]:

            device_ts = str(datetime.fromtimestamp(int(d["time"]) / 1000000000))
            recorded_ts = str(datetime.utcnow())
            x = d["values"]["x"]
            y = d["values"]["y"]
            z = d["values"]["z"]
            table_name = SENSOR_TO_TABLE_NAME.get(d.get("name"))
            

            with connection.cursor() as cursor:

                cursor.execute(f"""INSERT INTO {table_name} 
                (device_id,	session_id, device_timestamp, recorded_timestamp, x, y,	z) 
                VALUES (%s,%s,%s,%s,%s,%s,%s)""", 
                (device_id, session_id, device_ts, recorded_ts, x, y, z))

                connection.commit()