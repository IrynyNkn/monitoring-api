import requests
import logging
import uuid
from celery import Task
from typing import Any, Dict

from app.database.repositories.health_check_collected_data import IHealthCheckCollectedDataRepo
from app.database.repositories.health_check_config import IHealthCheckConfigRepository
from app.metrics.entities import HealthCheckConfig, ExtendedHCConfig
from app.routes.serializers import CreateHealthCheck


class HealthCheckService:
    def __init__(
        self,
        health_check_config_repo: IHealthCheckConfigRepository,
        health_check_task: Task,
        metrics_repository: IHealthCheckCollectedDataRepo,
    ) -> None:
        self._health_check_config_repo = health_check_config_repo
        self._health_check_task = health_check_task
        self._metrics_repository = metrics_repository

        self._logger = logging.getLogger(__name__)

    def perform_health_check(self, health_check_id: str):
        health_check_config = self.check_endpoint(health_check_id)

        if health_check_config is not None:
            self._logger.info(
                f"Performing continuous health check for {health_check_config.endpoint_url} {health_check_config.id}"
            )

            if not health_check_config.is_paused:
                response = requests.get(health_check_config.endpoint_url)
                rtt = response.elapsed.total_seconds()
                status = 1 if response.status_code // 100 == 2 else 0

                health_check_r = ExtendedHCConfig(
                    **health_check_config.to_dict(),
                    status=status,
                    round_trip_time=rtt
                )
                self._metrics_repository.save_health_check_data(health_check_r)

                self._health_check_task.apply_async(
                    args=[health_check_config.id],
                    countdown=health_check_config.interval,
                    expires=health_check_config.interval + 2
                )

                return
            else:
                self._logger.info(f"Ping to {health_check_id} is paused.")
        else:
            self._logger.info(f"Ping to {health_check_id} was canceled.")

    def initialize_health_check(
        self,
        owner_id: uuid,
        health_check: CreateHealthCheck,
    ):
        create_hc_id = self._create_health_check(owner_id, health_check)
        self._logger.info(f"Health check config for {health_check.endpoint_url} saved ...")

        self._health_check_task.delay(create_hc_id)

        return create_hc_id

    def get_health_check_metrics(self, health_check_id: str) -> Dict[str, Any]:
        health_check_metrics = self._metrics_repository.get_health_check_metrics(health_check_id)
        config = self.check_endpoint(health_check_id)

        health_check_metrics["metadata"]["interval"] = config.interval

        return health_check_metrics

    # POSTGRES DB
    def check_endpoint(self, health_check_id: str):
        health_check = self._health_check_config_repo.get(health_check_id)
        return health_check

    def get_health_checks_list(self, user_id: str):
        health_checks = self._health_check_config_repo.get_health_checks_by_user_id(user_id)
        return health_checks

    def _create_health_check(self, user_id: str, health_check: CreateHealthCheck):
        health_check_config = HealthCheckConfig(
            owner_id=user_id,
            endpoint_url=health_check.endpoint_url,
            interval=health_check.interval
        )

        created_hc_id = self._health_check_config_repo.save(health_check_config)
        self._logger.info(f"Health check config for {health_check.endpoint_url} saved ...")

        # self._ping_task.delay(ping_id)

        return created_hc_id

    def update_health_check(self, health_check_id: str, interval: int):
        updated_hc_id = self._health_check_config_repo.update_health_check(health_check_id, interval)
        return updated_hc_id

    def delete_health_check(self, health_check_id: str):
        deleted_hc_id = self._health_check_config_repo.delete(health_check_id)
        return deleted_hc_id
