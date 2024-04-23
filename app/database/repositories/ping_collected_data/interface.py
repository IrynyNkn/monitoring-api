from abc import ABC, abstractmethod
from icmplib import Host

from app.metrics.entities import ExtendedPingConfig


class IPingCollectedDataRepository(ABC):

    @abstractmethod
    def get_ping_metrics(self, ping_id: str):
        pass

    @abstractmethod
    def save_ping_data(self, ping_response: Host, entity: ExtendedPingConfig):
        pass
