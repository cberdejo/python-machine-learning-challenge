from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_BASE: str = "http://backend:8000/api/v1/mpc"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
