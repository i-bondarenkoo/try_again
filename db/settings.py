from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5457/try_again"
    db_echo: bool = True
    algorithm: str = "HS256"
    secret_key: str = "fc5aa915f53dc8ea6e75758dc26c03221b1d0e898d11d27c23a2644464d1bab3"
    access_token_expire_minutes: int = 5


settings = Settings()
