import logging
from icmplib import ping, Host

from app.settings import AppSettings


class ExternalPingService:
    def __init__(self, config: AppSettings):
        self._logger = logging.getLogger(__name__)
        self._config = config

    def ping(self):
        host = self._config.external_ping_host
        alert_email = self._config.external_ping_alert_email

        if host is None:
            return {"error": "Host not specified"}

        try:
            response = ping(host, count=1)
            status = 1 if response.packets_received > 0 else 0

            # if response.packets_received == 0:
            # send alert

            return {
                "round_trip_time": response.avg_rtt,
                "status": status,
                "host": host
            }
        except Exception as e:
            self._logger.error(f"Error during external ping execution {e}")
