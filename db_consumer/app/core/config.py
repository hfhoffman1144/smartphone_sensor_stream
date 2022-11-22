from starlette.config import Config

# Load .env file with config variables
config = Config(".env")

# Kafka config
PROJECT_NAME : str = config("PROJECT_NAME")
KAFKA_SERVER : str = config("KAFKA_SERVER")
TOPIC_NAME : str = config("TOPIC_NAME")

# QuestDB config
DB_USER : str = config("DB_USER")
DB_PASSWORD : str = config("DB_PASSWORD")
DB_HOST : str = config("DB_HOST")
DB_PORT : str = config("DB_PORT")
DB_NAME : str = config("DB_NAME")