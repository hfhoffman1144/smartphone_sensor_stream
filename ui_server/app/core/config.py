from pydantic import BaseSettings

# Load environment variables into a pydantic BaseSetting object
class AppConfig(BaseSettings):

    # QuestDB config
    DB_USER : str 
    DB_PASSWORD : str
    DB_HOST : str
    DB_PORT : str 
    DB_NAME : str
    DB_TRIAXIAL_OFFLOAD_TABLE_NAME : str

    # Application config
    UI_PORT : int

    # Misc config
    PHONE_SAMPLE_RATE : int

    class Config:

        case_sensitive = True

app_config = AppConfig()