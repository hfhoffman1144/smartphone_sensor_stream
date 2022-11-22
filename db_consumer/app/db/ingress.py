from datetime import datetime
from models.sensors import SensorName
import psycopg2 as pg

def create_connection(host:str, port:str, user_name:str, password:str, database:str):

    """Todo"""

    return pg.connect(user=user_name,
                      password=password,
                      host=host,
                      port=port,
                            database=DB_NAME,
                            options='-c statement_timeout=300000')

def write_acc(data:dict, connection):
    
    """
    Write phone accelerometer data to QuestDb 

    Parameters
    ----------
    data : dict
        The raw request data sent by the phone
    """

    session_id = data['sessionId']
    device_id = data['deviceId']
    
    for d in data['payload']:

        if d.get("name") == SensorName.ACC.value:

            ts = str(datetime.fromtimestamp(int(d["time"]) / 1000000000))
            x = d["values"]["x"]
            y = d["values"]["y"]
            z = d["values"]["z"]
            

            with connection.cursor() as cursor:

                cursor.execute("""INSERT INTO acc 
                (device_id,	session_id,	recorded_timestamp,	x,	y,	z) 
                VALUES (%s,%s,%s,%s,%s,%s)""", 
                (device_id, session_id, ts, x, y, z))

                connection.commit()