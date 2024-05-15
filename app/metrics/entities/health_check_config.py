from dataclasses import dataclass


@dataclass
class HealthCheckConfig:
    endpoint_url: str
    interval: int
    is_paused: bool = None
    id: str = None
    owner_id: str = None
    created_at: str = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "endpoint_url": self.endpoint_url,
            "is_paused": self.is_paused,
            "interval": self.interval,
            "created_at": str(self.created_at)
        }
