from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application
    app_name: str = "Purchases Service"
    debug: bool = False

    # Database
    database_url: str = "postgres://postgres:postgres@localhost:5432/purchases"

    # Redis
    redis_url: str = "redis://localhost:6379"

    # gRPC
    ambassador_grpc_host: str = "localhost"
    ambassador_grpc_port: int = 50051

    # Payme
    payme_id: str = ""
    payme_key: str = ""
    payme_is_test_mode: bool = True
    payme_account_field: str = "purchase_id"
    paytech_api_key: str = ""

    # Email - Mailgun
    mailgun_api_key: str = ""
    mailgun_domain: str = ""
    mailgun_from_email: str = "receipts@example.com"

    # Email - Dev (console output)
    email_backend: str = "console"  # "console" or "mailgun"

    # JWT
    jwt_secret: str = "your-secret-key"
    jwt_algorithm: str = "HS256"

    @property
    def ambassador_grpc_address(self) -> str:
        return f"{self.ambassador_grpc_host}:{self.ambassador_grpc_port}"


@lru_cache
def get_settings() -> Settings:
    return Settings()


# Tortoise ORM configuration
TORTOISE_ORM = {
    "connections": {
        "default": get_settings().database_url,
    },
    "apps": {
        "models": {
            "models": ["src.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
