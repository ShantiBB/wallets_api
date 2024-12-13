from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    postgres_name: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str


class DjangoSettings(BaseSettings):
    django_secret_key: str
    django_debug: bool
    django_allowed_hosts: list


class RedisSettings(BaseSettings):
    redis_host: str


class RabbitMQSettings(BaseSettings):
    rabbitmq_host: str


class Settings(
    PostgresSettings,
    DjangoSettings,
    RedisSettings,
    RabbitMQSettings
):
    model_config = SettingsConfigDict(
        env_file='.env'
    )


settings = Settings()
