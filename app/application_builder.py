from typing import Self, Optional

from celery import Celery
from fastapi import FastAPI, APIRouter
from redis import Redis

from app.application import Application
from app.settings import AppSettings


class ApplicationBuilder:
    def __init__(self, config: AppSettings) -> None:
        self.config = config

        self._fastapi_app = None
        self._celery_app = None
        self._redis = None

    @classmethod
    def from_config(cls, config: AppSettings) -> "ApplicationBuilder":
        return cls(config)

    def with_fastapi(self, override_with: Optional[FastAPI] = None) -> Self:
        self._fastapi_app = override_with or FastAPI()
        return self

    def with_fastapi_routes(self, routes: list[APIRouter], prefix: Optional[str] = None) -> Self:
        if not self._fastapi_app:
            raise ValueError("FastAPI is not configured")

        for route in routes:
            self._fastapi_app.include_router(route, prefix=prefix)

        return self

    def with_celery(self, override_with: Optional[Celery] = None) -> Self:
        self._celery_app = override_with or Celery()

        self._celery_app.conf.broker_url = self.config.celery_broker_url
        self._celery_app.conf.result_backend = self.config.celery_result_backend

        return self

    def with_redis(self, override_with: Optional[Redis] = None) -> Self:
        if override_with is None:
            self._redis = Redis(
                host=self.config.redis_host,
                port=self.config.redis_port,
                decode_responses=True,
                db=self.config.redis_app_db,
            )
        else:
            self._redis = override_with

        return self

    def build(self) -> Application:
        self._validate_application()

        return Application(
            config=self.config,
            fastapi=self._fastapi_app,
            celery=self._celery_app,
            redis=self._redis,
        )

    def _validate_application(self) -> None:
        if self._celery_app is None or self._fastapi_app is None or self._redis is None:
            raise ValueError("All applications must be configured")
