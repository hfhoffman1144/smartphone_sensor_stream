from pydantic import BaseSettings

# Load environment variables into a pydantic BaseSetting object
class AppConfig(BaseSettings):

    # QuestDB config
    DB_USER : str = "admin"
    DB_PASSWORD : str = "quest"
    DB_HOST : str = "127.0.0.1"
    DB_PORT : str = "8812"
    DB_NAME : str = "qdb"
    DB_TRIAXIAL_OFFLOAD_TABLE_NAME = "device_offload"

    # Application config
    UI_PORT : int = 8080

    # Misc config
    PHONE_SAMPLE_RATE : int = 50

    class Config:

        case_sensitive = True

app_config = AppConfig()