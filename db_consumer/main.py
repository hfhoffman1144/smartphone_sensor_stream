import asyncio
import json
from enum import Enum
from datetime import datetime
import psycopg2 as pg
from aiokafka import AIOKafkaConsumer


class SensorName(Enum):
    
    ACC = 'accelerometeruncalibrated'
    GYRO = 'gyroscopeuncalibrated'

TOPIC_NAME = "phone-stream"
KAFKA_SERVER = "localhost:9093"

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

    
async def consume_messages() -> None:

    connection = pg.connect(user="admin",
                            password="quest",
                            host="127.0.0.1",
                            port="8812",
                            database="qdb",
                            options='-c statement_timeout=300000')
   
    loop = asyncio.get_event_loop()
    consumer = AIOKafkaConsumer(
        TOPIC_NAME,
        loop=loop,
        client_id='Phone Stream Producer',
        bootstrap_servers=KAFKA_SERVER,
        enable_auto_commit=False,
    )

    await consumer.start()
    try:
        async for msg in consumer:
            print(msg.value)
            print('################')
            write_acc(json.loads(msg.value), connection)
    finally:
        await consumer.stop()
        connection.close()

async def main():

    await consume_messages()

asyncio.run(main())




