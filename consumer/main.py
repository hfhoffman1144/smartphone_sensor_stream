from kafka import KafkaConsumer
from json import loads
from enum import Enum
from questdb.ingress import Sender
from datetime import datetime


class SensorName(Enum):
    
    ACC = 'accelerometeruncalibrated'
    GYRO = 'gyroscopeuncalibrated'

TOPIC_NAME = "phone-stream"
KAFKA_SERVER = "localhost:9093"

def write_acc(data:dict, db_host:str, db_port:int, table_name:str):
    
    """
    Write phone accelerometer data to QuestDb 

    Parameters
    ----------
    data : dict
        The raw request data sent by the phone
    db_host : str
        The QuestDb host
    db_port: int
        The QuestDb port
    table_name : str
        The table to write to
    """

    session_id = data['sessionId']
    device_id = data['deviceId']

    for d in data['payload']:

        if d.get("name") == SensorName.ACC.value:

            ts = datetime.fromtimestamp(d["time"] / 1000000000)
            x = d["values"]["x"]
            y = d["values"]["y"]
            z = d["values"]["z"]
            

            with Sender(db_host, db_port) as sender:

                sender.row(
                    table_name,
                    symbols={'device_id':str(device_id),'session_id': str(session_id)},
                    columns={'recorded_timestamp': str(ts) , 'x':x, 'y':y, 'z':z})
                sender.flush()


consumer = KafkaConsumer(
     TOPIC_NAME,
     bootstrap_servers=[KAFKA_SERVER],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')))

for message in consumer:
    message = message.value
    write_acc(message, "localhost", 9009, "acc")
    print(message)
    print('###########################')
    