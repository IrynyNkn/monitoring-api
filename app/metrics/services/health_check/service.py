import logging

from app.database.repositories.health_check_config import IHealthCheckConfigRepository
from app.metrics.entities import HealthCheckConfig
from app.routes.serializers import CreateHealthCheck


class HealthCheckService:
    def __init__(
        self,
        health_check_repo: IHealthCheckConfigRepository,
        # health_check_task: Task,
        # metrics_repository: IPingCollectedDataRepository,
    ) -> None:
        self._health_check_repo = health_check_repo
        # self._metrics_repository = metrics_repository
        # self._health_check_task = health_check_task

        self._logger = logging.getLogger(__name__)

    def check_endpoint(self, health_check_id: str):
        health_check = self._health_check_repo.get(health_check_id)
        return health_check

    def get_health_checks_list(self, user_id: str):
        health_checks = self._health_check_repo.get_health_checks_by_user_id(user_id)
        return health_checks

    def create_health_check(self, user_id: str, health_check: CreateHealthCheck):
        health_check_config = HealthCheckConfig(
            owner_id=user_id,
            endpoint_url=health_check.endpoint_url,
            interval=health_check.interval
        )

        created_hc_id = self._health_check_repo.save(health_check_config)
        self._logger.info(f"Health check config for {health_check.endpoint_url} saved ...")

        # self._ping_task.delay(ping_id)

        return created_hc_id

    def update_health_check(self, health_check_id: str, interval: int):
        updated_hc_id = self._health_check_repo.update_health_check(health_check_id, interval)
        return updated_hc_id

    def delete_health_check(self, health_check_id: str):
        deleted_hc_id = self._health_check_repo.delete(health_check_id)
        return deleted_hc_id
