from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5457/try_again"
    db_echo: bool = True


settings = Settings()
