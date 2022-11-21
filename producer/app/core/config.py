from starlette.config import Config

# Load .env file with config variables
config = Config(".env")

PROJECT_NAME : str = config("PROJECT_NAME")
KAFKA_SERVER : str = config("KAFKA_SERVER")
TOPIC_NAME : str = config("TOPIC_NAME")