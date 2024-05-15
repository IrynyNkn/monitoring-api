from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any

from app.metrics.entities import HealthCheckConfig


class IHealthCheckConfigRepository(ABC):
    @abstractmethod
    def get(self, health_check_id: str) -> Optional[HealthCheckConfig]:
        pass

    @abstractmethod
    def save(self, entity: HealthCheckConfig) -> str:
        pass

    @abstractmethod
    def delete(self, health_check_id: str) -> Optional[str]:
        pass

    @abstractmethod
    def update_health_check(self, health_check_id: str, interval: int) -> Optional[str]:
        pass

    @abstractmethod
    def get_health_checks_by_user_id(self, user_id: str) -> List[Dict[str, Any]]:
        pass
