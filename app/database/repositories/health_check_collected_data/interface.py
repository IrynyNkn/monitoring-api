from abc import ABC, abstractmethod
from typing import Any, Dict

from app.metrics.entities.health_check_config import ExtendedHCConfig


class IHealthCheckCollectedDataRepo(ABC):
    @abstractmethod
    def get_health_check_metrics(self, health_check_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def save_health_check_data(self, entity: ExtendedHCConfig):
        pass

    @abstractmethod
    def _get_health_check_metadata(self, health_check_id: str) -> Dict[str, Any]:
        pass
