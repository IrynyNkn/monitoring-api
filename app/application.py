from typing import cast

from celery import Celery, Task
from fastapi import FastAPI
from redis import Redis
from influxdb_client import InfluxDBClient

from app.settings import AppSettings
from app.database.repositories import (
    IPingConfigRepository,
    PingConfigRedisRepository,
    IPingCollectedDataRepository,
    PingCollectedDataRepository
)
from app.metrics.icmp_ping.service import PingService


class Application:
    config: AppSettings
    redis: Redis
    celery: Celery
    fastapi: FastAPI
    influxdb_client: InfluxDBClient

    def __init__(
        self,
        config: AppSettings,
        redis: Redis,
        celery: Celery,
        fastapi: FastAPI,
        influxdb_client: InfluxDBClient
    ) -> None:
        self.config = config
        self.redis = redis
        self.celery = celery
        self.fastapi = fastapi
        self.influxdb_client = influxdb_client

        self._ping_repository = None
        self._ping_service = None

        self._metrics_repository = None
        self._metrics_service = None

    @property
    def ping_repository(self) -> IPingConfigRepository:
        if not self._ping_repository:
            self._ping_repository = PingConfigRedisRepository(self.redis)

        return self._ping_repository

    @property
    def ping_service(self) -> PingService:
        if not self._ping_service:
            from .metrics.celery_tasks import continuous_ping
            self._ping_service = PingService(self.ping_repository, cast(Task, continuous_ping), self.metrics_repository)

        return self._ping_service

    @property
    def metrics_repository(self) -> IPingCollectedDataRepository:
        if not self._metrics_repository:
            self._metrics_repository = PingCollectedDataRepository(self.influxdb_client, self.config)

        return self._metrics_repository
