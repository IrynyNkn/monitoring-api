import logging
import uuid
from typing import Any, Dict, List, Optional

from icmplib import ping, Host
from celery import Task

from app.database.repositories import IPingConfigRepository, IPingCollectedDataRepository
from app.metrics.entities import PingConfig, ExtendedPingConfig
from app.metrics.services.notifications.alerts import AlertsService
from app.routes.serializers import AlertGroup
from app.metrics.entities.alert import Alert as AlertEntity


class PingService:
    def __init__(
        self,
        ping_repository: IPingConfigRepository,
        ping_task: Task,
        metrics_repository: IPingCollectedDataRepository,
        alerts_service: AlertsService,
    ) -> None:
        self._ping_repository = ping_repository
        self._metrics_repository = metrics_repository
        self._ping_task = ping_task
        self._alerts_service = alerts_service

        self._logger = logging.getLogger(__name__)

    def _send_alert(self, ping_config: PingConfig):
        configured_alerts = self._alerts_service.get_alerts(ping_config.owner_id)
        alert = next(
            (alert for alert in configured_alerts if alert['alert_group'] == AlertGroup.ICMP_PING),
            None,
        )

        if alert:
            self._alerts_service.send_alert(ping_config, AlertEntity(**alert))

    def ping(self, ping_id: str) -> None:
        ping_config = self._ping_repository.get(ping_id)

        if ping_config is not None:
            self._logger.info(f"Performing continuous ping for {ping_config.host} {ping_config.id}")

            if not ping_config.is_paused:
                try:
                    response = ping(ping_config.host, count=1)
                    self._save_ping_response(response, ping_config)

                    if response.packets_received == 0:
                        self._send_alert(ping_config)
                except Exception as e:
                    self._logger.error(f"Error during ping execution {ping_config.host} {ping_config.id}")
                    self._send_alert(ping_config)

            self._ping_task.apply_async(
                args=[ping_config.id],
                countdown=ping_config.interval,
                expires=ping_config.interval + 2
            )
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
            is_paused=False,
            owner_id=owner_id
        )

        ping_id = self._ping_repository.save(ping_config)

        self._logger.info(f"Ping config for {host} saved ...")

        self._ping_task.delay(ping_id)

        return ping_id

    def get_ping_metrics(self, ping_id: str, time_range_raw: str) -> Dict[str, Any]:
        time_range = time_range_raw if time_range_raw is not None else '-12h'
        ping_metrics = self._metrics_repository.get_ping_metrics(ping_id, time_range)

        ping_config = self._ping_repository.get(ping_id)
        ping_metrics['metadata']['interval'] = ping_config.interval
        ping_metrics['metadata']['is_paused'] = ping_config.is_paused

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

    def pause_ping(self, ping_id: str):
        ping_id = self._ping_repository.pause_ping(ping_id, True)
        return ping_id

    def resume_ping(self, ping_id: str):
        ping_id = self._ping_repository.pause_ping(ping_id, False)
        return ping_id

    def delete_ping(self, ping_id: str) -> Optional[str]:
        deleted_ping_id = self._ping_repository.delete(ping_id)
        return deleted_ping_id
