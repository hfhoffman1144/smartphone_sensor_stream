from pydantic import BaseSettings

# Load .env file with config variables into a pydantic BaseSetting object
class AppConfig(BaseSettings):

    # Kafka config
    PROJECT_NAME : str
    KAFKA_SERVER : str
    TOPIC_NAME : str

    # QuestDB config
    DB_USER : str
    DB_PASSWORD : str 
    DB_HOST : str 
    DB_PORT : str 
    DB_NAME : str 

    class Config:

        env_file = ".env"

app_config = AppConfig()