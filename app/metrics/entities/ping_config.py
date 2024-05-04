from dataclasses import dataclass


@dataclass
class PingConfig:
    host: str
    interval: int
    is_paused: bool
    id: str = None
    owner_id: str = None
    created_at: str = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "host": self.host,
            "is_paused": self.is_paused,
            "interval": self.interval,
            "created_at": str(self.created_at)
        }


@dataclass
class ExtendedPingConfig(PingConfig):
    round_trip_time: float = None

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict["round_trip_time"] = self.round_trip_time
        return base_dict
