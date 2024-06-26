from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any

from app.metrics.entities.ping_config import PingConfig


class IPingConfigRepository(ABC):
    @abstractmethod
    def get(self, ping_id: str) -> Optional[PingConfig]:
        pass

    @abstractmethod
    def save(self, entity: PingConfig) -> str:
        pass

    @abstractmethod
    def delete(self, ping_id: str) -> None:
        pass

    @abstractmethod
    def update_ping(self, ping_id: str, interval: int) -> Optional[str]:
        pass

    @abstractmethod
    def get_pings_by_user_id(self, user_id: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def pause_ping(self, ping_id: str, pause_value: bool) -> Optional[str]:
        pass
