from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_type: str = (
        "inmemory"  # would defualt to "postgresql+asyncpg" or "mongo" for live API
    )

    model_config = {"env_file": ".env"}

    model_config = SettingsConfigDict(extra="allow", env_file=".env")


settings: Settings = Settings()
