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
