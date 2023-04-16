import asyncio
import json
from aiokafka import AIOKafkaConsumer
from core.config import app_config
from db.ingress import (create_connection,
                        create_triaxial_table,
                        write_triaxial_sensor_data)


async def consume_messages() -> None:

    """
    Coroutine to consume smart phone sensor messages from a kafka topic
    """

    # Create a QuestDB connection
    connection = create_connection(host=app_config.DB_HOST,
                                   port=app_config.DB_PORT,
                                   user_name=app_config.DB_USER,
                                   password=app_config.DB_PASSWORD,
                                   database=app_config.DB_NAME)
    
    # Instantiate consumer
    consumer = AIOKafkaConsumer(
        app_config.TOPIC_NAME,
        client_id='db_consumer',
        group_id='db_consumer',
        bootstrap_servers=app_config.KAFKA_URL,
        enable_auto_commit=False,  # why?
    )

    await consumer.start()
    try:
        async for msg in consumer:
            # Format each message in the log and write to QuestDB
            write_triaxial_sensor_data(json.loads(msg.value), app_config.DB_IMP_URL, app_config.DB_TRIAXIAL_OFFLOAD_TABLE_NAME)
    finally:
        await consumer.stop()
        connection.close()

async def main():

    await consume_messages()

if __name__ == "__main__":

    # Create the table to store triaxial sensor data if it doesn't exist
    connection = create_connection(host=app_config.DB_HOST,
                                    port=app_config.DB_PORT,
                                    user_name=app_config.DB_USER,
                                    password=app_config.DB_PASSWORD,
                                    database=app_config.DB_NAME)

    create_triaxial_table(app_config.DB_TRIAXIAL_OFFLOAD_TABLE_NAME, connection)

    asyncio.run(main())




