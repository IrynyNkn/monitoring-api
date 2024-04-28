from abc import ABC, abstractmethod
from typing import Any


class IKubeCollectedDataRepository(ABC):
    @abstractmethod
    def _save_node_data(self, entity: dict[str, Any]):
        pass

    @abstractmethod
    def _save_pod_data(self, entity: dict[str, Any]):
        pass

    @abstractmethod
    def save_kube_data(self, node_data: dict[str, Any], pod_data: dict[str, Any]) -> None:
        pass
