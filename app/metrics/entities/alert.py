from dataclasses import dataclass

from app.routes.serializers import AlertGroup, AlertType


@dataclass
class Alert:
    id: str
    email: str
    for_: int
    repeat_alert: int
    alert_group: AlertGroup
    alert_type: AlertType
    owner_id: str = None
    created_at: str = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "for_": self.for_,
            "repeat_alert": self.repeat_alert,
            "alert_group": str(self.alert_group),
            "alert_type": str(self.alert_type)
        }
