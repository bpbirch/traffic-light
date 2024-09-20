from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_type: str = "postgresql+asyncpg"  # alternate: "inmemory"
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int
    jwt_refresh_token_expire_days: int
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_s3_region: str = "us-east-2"
    aws_s3_resume_bucket_name: str = "traffic-light-s3-storage"

    model_config = {
        "env_file": ".env"
    }

    model_config = SettingsConfigDict(
        extra="allow",
        env_file=".env"
    )


settings: Settings = Settings()
