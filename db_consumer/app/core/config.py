from pydantic import BaseSettings, validator

# Load environment variables into a pydantic BaseSetting object
class AppConfig(BaseSettings):

    # Kafka config
    PROJECT_NAME : str
    KAFKA_PORT : str
    KAFKA_HOST : str
    TOPIC_NAME : str
    KAFKA_URL : str = ""

    # QuestDB config
    DB_USER : str
    DB_PASSWORD : str 
    DB_HOST : str 
    DB_PORT : str 
    DB_IMP_PORT : str
    DB_NAME : str 
    DEVICE_OFFLOAD_TBL_NAME : str
    DB_IMP_URL : str =  ""

    class Config:

        case_sensitive = True

    @validator("KAFKA_URL", pre=True, always=True)
    def set_kafka_url(cls, v, values, **kwargs):
        return values['KAFKA_HOST'] + ":" + values['KAFKA_PORT'] 

    @validator("DB_IMP_URL", pre=True, always=True)
    def set_db_imp_url(cls, v, values, **kwargs):
        return "http://" + values['DB_HOST'] + ":" + values['DB_IMP_PORT'] + '/imp'

app_config = AppConfig()