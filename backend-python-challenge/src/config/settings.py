from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # General settings
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # MinIO
    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str

    # External API
    DATA_SERVICE_URL: str = "http://data_service:8777"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
