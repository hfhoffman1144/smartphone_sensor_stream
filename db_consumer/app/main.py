import asyncio
import json
from aiokafka import AIOKafkaConsumer
from core.config import app_config
from db.ingress import (create_connection,
                        create_triaxial_table,
                        write_sensor_payloads,
                        SENSOR_TO_TABLE_NAME)


async def consume_messages() -> None:

    """
    Coroutine to consume smart phone sensor messages from kafka topic
    """

    connection = create_connection(host=app_config.DB_HOST,
                                   port=app_config.DB_PORT,
                                   user_name=app_config.DB_USER,
                                   password=app_config.DB_PASSWORD,
                                   database=app_config.DB_NAME)
   
    loop = asyncio.get_event_loop()
    consumer = AIOKafkaConsumer(
        app_config.TOPIC_NAME,
        loop=loop,
        client_id='all',
        bootstrap_servers=app_config.KAFKA_SERVER,
        enable_auto_commit=False,
    )

    await consumer.start()
    try:
        async for msg in consumer:
            print(msg.value)
            print('################')
            write_sensor_payloads(json.loads(msg.value), connection)
    finally:
        await consumer.stop()
        connection.close()

async def main():

    await consume_messages()

if __name__ == "__main__":

    # Create tables to store triaxial sensor data if they don't exist
    for table_name in SENSOR_TO_TABLE_NAME.values():

        connection = create_connection(host=app_config.DB_HOST,
                                       port=app_config.DB_PORT,
                                       user_name=app_config.DB_USER,
                                       password=app_config.DB_PASSWORD,
                                       database=app_config.DB_NAME)

        create_triaxial_table(table_name, connection)

    asyncio.run(main())




