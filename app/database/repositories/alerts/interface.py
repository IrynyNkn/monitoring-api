from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

from app.metrics.entities.alert import Alert
from app.routes.serializers import CreateAlert


class IAlertsRepository(ABC):
    @abstractmethod
    def get_alerts(self, user_id: str) -> Optional[List[Dict[str, Any]]]:
        pass

    @abstractmethod
    def create_alert(self, entity: CreateAlert, user_id: str) -> Optional[str]:
        pass

    @abstractmethod
    def update_alert(self, entity, alert_id: str) -> Optional[str]:
        pass

    @abstractmethod
    def delete_alert(self, alert_id: str) -> Optional[str]:
        pass
