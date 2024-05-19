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


@dataclass
class ExtendedHCConfig(HealthCheckConfig):
    round_trip_time: float = None
    status: int = None

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict["round_trip_time"] = self.round_trip_time

        return base_dict
