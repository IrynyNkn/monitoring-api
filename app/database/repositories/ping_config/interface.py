from abc import ABC, abstractmethod
from typing import Optional

from app.metrics.entities.ping_config import PingConfig


class IPingConfigRepository(ABC):
    @abstractmethod
    def get(self, ping_id: str) -> Optional[PingConfig]:
        pass

    @abstractmethod
    def save(self, entity: PingConfig) -> None:
        pass

    @abstractmethod
    def delete(self, ping_id: str) -> None:
        pass
