# Конфигурация проекта
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    JWT_SECRET: str
    MAPBOX_TOKEN: str
    STRIPE_KEY: str = ""
    WEATHER_API: str = ""
    FUEL_API: str = ""

    class Config:
        env_file = ".env"

settings = Settings()

