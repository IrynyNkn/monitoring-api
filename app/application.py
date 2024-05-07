from typing import cast

from celery import Celery, Task
from fastapi import FastAPI
from redis import Redis
from influxdb_client import InfluxDBClient
from sqlalchemy.orm import sessionmaker, Session

from app.database.repositories.user.user_repository import UserRepository
from app.metrics.services.accounts.user_service import UserService
from app.settings import AppSettings
from app.database.repositories import (
    IPingConfigRepository,
    PingConfigRepository,
    IPingCollectedDataRepository,
    PingCollectedDataRepository,
    IKubeCollectedDataRepository,
    KubeCollectedDataRepository,
)
from app.metrics.services.icmp_ping import PingService
from app.metrics.services.kube_metrics import KubeMetricsService
from app.metrics.services.notifications import EmailNotifier


class Application:
    config: AppSettings
    redis: Redis
    celery: Celery
    fastapi: FastAPI
    influxdb_client: InfluxDBClient
    postgres_session_maker: sessionmaker[Session]

    def __init__(
        self,
        config: AppSettings,
        redis: Redis,
        celery: Celery,
        fastapi: FastAPI,
        influxdb_client: InfluxDBClient,
        postgres_session_maker: sessionmaker[Session],
    ) -> None:
        self.config = config
        self.redis = redis
        self.celery = celery
        self.fastapi = fastapi
        self.influxdb_client = influxdb_client
        self.postgres_session_maker = postgres_session_maker

        self._ping_repository = None
        self._ping_service = None

        self._metrics_repository = None
        self._metrics_service = None

        self._kube_metrics_repository = None
        self._kube_metrics_service = None

        self._user_service = None
        self._user_repository = None

        self._notification_service = None

    @property
    def ping_repository(self) -> IPingConfigRepository:
        return PingConfigRepository(self.postgres_session_maker())

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

    @property
    def kube_metrics_service(self) -> KubeMetricsService:
        if not self._kube_metrics_service:
            from .metrics.celery_tasks import kube_metrics_collecting
            self._kube_metrics_service = KubeMetricsService(
                self.kube_metrics_repository,
                cast(Task, kube_metrics_collecting)
            )

        return self._kube_metrics_service

    @property
    def kube_metrics_repository(self) -> IKubeCollectedDataRepository:
        if not self._kube_metrics_repository:
            self._kube_metrics_repository = KubeCollectedDataRepository(self.influxdb_client, self.config)

        return self._kube_metrics_repository

    @property
    def user_repository(self) -> UserRepository:
        return UserRepository(session=self.postgres_session_maker())

    @property
    def user_service(self) -> UserService:
        if not self._user_service:
            self._user_service = UserService(self.user_repository)

        return self._user_service

    @property
    def notification_service(self) -> EmailNotifier:
        if not self._notification_service:
            self._notification_service = EmailNotifier(self.config.smtp_settings)

        return self._notification_service
