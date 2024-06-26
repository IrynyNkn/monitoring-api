from typing import Optional

from celery import Celery
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from redis import Redis
from influxdb_client import InfluxDBClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.application import Application
from app.settings import AppSettings


class ApplicationBuilder:
    def __init__(self, config: AppSettings) -> None:
        self.config = config

        self._fastapi_app = None
        self._celery_app = None
        self._redis = None
        self._influxdb_client = None
        self._postgres_session_maker = None

    @classmethod
    def from_config(cls, config: AppSettings) -> "ApplicationBuilder":
        return cls(config)

    def with_fastapi(self, override_with: Optional[FastAPI] = None) -> "ApplicationBuilder":
        self._fastapi_app = override_with or FastAPI()
        self._fastapi_app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        return self

    def with_fastapi_routes(self, routes: list[APIRouter], prefix: Optional[str] = None) -> "ApplicationBuilder":
        if not self._fastapi_app:
            raise ValueError("FastAPI is not configured")

        for route in routes:
            self._fastapi_app.include_router(route, prefix=prefix)

        return self

    def with_celery(self, override_with: Optional[Celery] = None) -> "ApplicationBuilder":
        self._celery_app = override_with or Celery()

        self._celery_app.conf.broker_url = self.config.celery_broker_url
        self._celery_app.conf.result_backend = self.config.celery_result_backend

        return self

    def with_redis(self, override_with: Optional[Redis] = None) -> "ApplicationBuilder":
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

    def with_influxdb(self, override_with: Optional[InfluxDBClient] = None) -> "ApplicationBuilder":
        if override_with is None:
            self._influxdb_client = InfluxDBClient(
                url=self.config.influxdb_url,
                token=self.config.influxdb_admin_token,
                org=self.config.influxdb_org
            )
        else:
            self._influxdb_client = override_with

        return self

    def with_postgres(self, override_with: None = None) -> "ApplicationBuilder":
        engine = create_engine(AppSettings().postgres_url)
        session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self._postgres_session_maker = scoped_session(session_factory)

        return self

    def build(self) -> Application:
        return Application(
            config=self.config,
            fastapi=self._fastapi_app,
            celery=self._celery_app,
            redis=self._redis,
            influxdb_client=self._influxdb_client,
            postgres_session_maker=self._postgres_session_maker,
        )
