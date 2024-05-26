from pydantic import Field
from pydantic_settings import BaseSettings


class SMTPSettings(BaseSettings):
    host: str = Field(..., alias="SMTP_HOST")
    port: int = Field(..., alias="SMTP_PORT")
    username: str = Field(..., alias="SMTP_USERNAME")
    password: str = Field(..., alias="SMTP_PASSWORD")


class AppSettings(BaseSettings):
    celery_broker_url: str = Field(..., alias="CELERY_BROKER_URL")
    celery_result_backend: str = Field(..., alias="CELERY_RESULT_BACKEND")

    redis_host: str = Field(..., alias="REDIS_HOST")
    redis_port: int = Field(..., alias="REDIS_PORT")
    redis_app_db: int = Field(..., alias="REDIS_APP_DB")

    influxdb_url: str = Field(..., alias="INFLUXDB_URL")
    influxdb_username: str = Field(..., alias="DOCKER_INFLUXDB_INIT_USERNAME")
    influxdb_password: str = Field(..., alias="DOCKER_INFLUXDB_INIT_PASSWORD")
    influxdb_org: str = Field(..., alias="DOCKER_INFLUXDB_INIT_ORG")
    influxdb_bucket: str = Field(..., alias="DOCKER_INFLUXDB_INIT_BUCKET")
    influxdb_admin_token: str = Field(..., alias="DOCKER_INFLUXDB_INIT_ADMIN_TOKEN")

    postgres_url: str = Field(..., alias="POSTGRES_URL")

    secret_key: str = Field(..., alias="SECRET_KEY")
    auth_enabled: bool = Field(True, alias="AUTH_ENABLED")
    token_life_minutes: int = Field(720, alias="TOKEN_LIFE_MINUTES")  # in minutes

    gather_kube_metrics: bool = Field(True, alias="GATHER_KUBE_METRICS")

    smtp_settings: SMTPSettings = SMTPSettings()

    is_external: bool = Field(False, alias="IS_EXTERNAL")
