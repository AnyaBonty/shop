from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    class Config:
        env_file = "backend/.env"
        env_file_encoding = "utf-8"

settings = Settings()