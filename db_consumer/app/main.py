import asyncio
import json
from aiokafka import AIOKafkaConsumer
from core.config import (KAFKA_SERVER,
                         TOPIC_NAME,
                         DB_USER,
                         DB_PASSWORD,
                         DB_HOST,
                         DB_PORT,
                         DB_NAME)
                         
from db.ingress import write_acc


async def consume_messages() -> None:

    connection = pg.connect(user=DB_USER,
                            password=DB_PASSWORD,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME,
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




