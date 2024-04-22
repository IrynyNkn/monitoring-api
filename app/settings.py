from pydantic import Field
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    celery_broker_url: str = Field(..., alias="CELERY_BROKER_URL")
    celery_result_backend: str = Field(..., alias="CELERY_RESULT_BACKEND")

    redis_host: str = Field(..., alias="REDIS_HOST")
    redis_port: int = Field(..., alias="REDIS_PORT")
    redis_app_db: int = Field(..., alias="REDIS_APP_DB")
