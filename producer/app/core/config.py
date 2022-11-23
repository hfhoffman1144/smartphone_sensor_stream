from pydantic import BaseSettings

# Load .env file with config variables into a pydantic BaseSetting object
class AppConfig(BaseSettings):

    PROJECT_NAME : str 
    KAFKA_SERVER : str 
    TOPIC_NAME : str 

    class Config:

        env_file = ".env"

app_config = AppConfig()




