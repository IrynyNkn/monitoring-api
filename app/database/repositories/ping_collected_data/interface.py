from abc import ABC, abstractmethod
from typing import Any, Dict
from icmplib import Host

from app.metrics.entities import ExtendedPingConfig


class IPingCollectedDataRepository(ABC):

    @abstractmethod
    def get_ping_metrics(self, ping_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def save_ping_data(self, ping_response: Host, entity: ExtendedPingConfig):
        pass

    @abstractmethod
    def _get_ping_metadata(self, ping_id: str) -> Dict[str, Any]:
        pass
