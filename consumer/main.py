from kafka import KafkaConsumer
from json import loads

TOPIC_NAME = "phone-stream"
KAFKA_SERVER = "localhost:9093"

consumer = KafkaConsumer(
     TOPIC_NAME,
     bootstrap_servers=[KAFKA_SERVER],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')))

for message in consumer:
    message = message.value
    print(message)