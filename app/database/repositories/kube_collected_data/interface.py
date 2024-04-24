from abc import ABC, abstractmethod


class IKubeCollectedDataRepository(ABC):
    @abstractmethod
    def save_kube_data(self):
        pass
