from dataclasses import dataclass


@dataclass
class PingConfig:
    id: str
    host: str
    status: str
    interval: int

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "host": self.host,
            "status": self.status,
            "interval": self.interval,
        }


@dataclass
class ExtendedPingConfig(PingConfig):
    round_trip_time: float

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict["round_trip_time"] = self.round_trip_time
        return base_dict
