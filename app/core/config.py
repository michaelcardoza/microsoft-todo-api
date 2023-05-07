from functools import lru_cache

from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    database_url: PostgresDsn
    jwt_secret: str
    jwt_expiration_days: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
