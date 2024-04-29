from dataclasses import dataclass


@dataclass
class PingConfig:
    host: str
    interval: int
    status: str = None
    id: str = None
    owner_id: str = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "host": self.host,
            "status": self.status,
            "interval": self.interval,
        }


@dataclass
class ExtendedPingConfig(PingConfig):
    round_trip_time: float = None

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict["round_trip_time"] = self.round_trip_time
        return base_dict
