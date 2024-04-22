from typing import cast

from celery import Celery, Task
from fastapi import FastAPI
from redis import Redis

from app.settings import AppSettings
from app.database.repositories import IPingConfigRepository, PingConfigRedisRepository
from app.metrics.icmp_ping.service import PingService


class Application:
    config: AppSettings
    redis: Redis
    celery: Celery
    fastapi: FastAPI

    def __init__(
        self,
        config: AppSettings,
        redis: Redis,
        celery: Celery,
        fastapi: FastAPI,
    ) -> None:
        self.config = config
        self.redis = redis
        self.celery = celery
        self.fastapi = fastapi

        self._ping_repository = None
        self._ping_service = None

    @property
    def ping_repository(self) -> IPingConfigRepository:
        if not self._ping_repository:
            self._ping_repository = PingConfigRedisRepository(self.redis)

        return self._ping_repository

    @property
    def ping_service(self) -> PingService:
        if not self._ping_service:
            from .metrics.celery_tasks import continuous_ping
            self._ping_service = PingService(self.ping_repository, cast(Task, continuous_ping))

        return self._ping_service
