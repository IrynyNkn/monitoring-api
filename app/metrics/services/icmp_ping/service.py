import logging
import uuid
from typing import Any, Dict, List, Optional

from icmplib import ping, Host
from celery import Task

from app.database.repositories import IPingConfigRepository, IPingCollectedDataRepository
from app.metrics.entities import PingConfig, ExtendedPingConfig


class PingService:
    def __init__(
        self,
        ping_repository: IPingConfigRepository,
        ping_task: Task,
        metrics_repository: IPingCollectedDataRepository,
    ) -> None:
        self._ping_repository = ping_repository
        self._metrics_repository = metrics_repository
        self._ping_task = ping_task

        self._logger = logging.getLogger(__name__)

    def ping(self, ping_id: str) -> None:
        ping_config = self._ping_repository.get(ping_id)

        if ping_config is not None:
            self._logger.info(f"Performing continuous ping for {ping_config.host} {ping_config.id}")

            if ping_config.status == "active":
                response = ping(ping_config.host, count=1)

                self._save_ping_response(response, ping_config)

                self._ping_task.apply_async(
                    args=[ping_config.id],
                    countdown=ping_config.interval,
                )

                return
        else:
            self._logger.info(f"Ping to {ping_id} was canceled.")

    def add_new_ping(
        self,
        host: str,
        interval: int,
        owner_id: uuid
    ) -> str:
        ping_config = PingConfig(
            host=host,
            interval=interval,
            status="active",
            owner_id=owner_id
        )

        ping_id = self._ping_repository.save(ping_config)

        self._logger.info(f"Ping config for {host} saved ...")

        self._ping_task.delay(ping_id)

        return ping_id

    def get_ping_metrics(self, ping_id: str) -> Dict[str, Any]:
        ping_metrics = self._metrics_repository.get_ping_metrics(ping_id)
        return ping_metrics

    def get_pings(self, user_id: str) -> List[Dict[str, Any]]:
        pings = self._ping_repository.get_pings_by_user_id(user_id)
        return pings

    def _save_ping_response(self, response: Host, config: PingConfig) -> None:
        ping_data = ExtendedPingConfig(
            **config.to_dict(),
            round_trip_time=response.avg_rtt
        )
        self._metrics_repository.save_ping_data(response, ping_data)

    def update_ping(self, ping_id: str, interval: int):
        ping_id = self._ping_repository.update_ping(ping_id, interval)
        return ping_id

    def delete_ping(self, ping_id: str) -> Optional[str]:
        try:
            uuid.UUID(ping_id, version=4)
        except ValueError:
            return None

        deleted_ping_id = self._ping_repository.delete(ping_id)
        return deleted_ping_id
