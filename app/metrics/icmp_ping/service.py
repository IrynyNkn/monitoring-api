import logging
import uuid
from typing import Any, Dict

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
            self._logger.info(f"Performing continuous ping for {ping_config.id}")

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
    ) -> str:
        ping_config = PingConfig(
            id=uuid.uuid4().hex,
            host=host,
            interval=interval,
            status="active",
        )

        self._ping_repository.save(ping_config)

        self._logger.info(f"Ping config for {host} saved ...")

        self._ping_task.delay(ping_config.id)

        return ping_config.id

    def get_ping_metrics(self, ping_id: str) -> Dict[str, Any]:
        ping_metrics = self._metrics_repository.get_ping_metrics(ping_id)
        return ping_metrics

    # def get_pings(self):
        # pings = self._metrics_repository.get_user_pings()
        # return pings

    def _save_ping_response(self, response: Host, config: PingConfig) -> None:
        ping_data = ExtendedPingConfig(
            **config.to_dict(),
            round_trip_time=response.avg_rtt
        )
        self._metrics_repository.save_ping_data(response, ping_data)
