from app.database.repositories import AlertRepository
from app.routes.serializers import CreateAlert


class AlertsService:
    def __init__(self, alert_repository: AlertRepository) -> None:
        self._alert_repository = alert_repository

    def get_alerts(self, user_id: str):
        alerts = self._alert_repository.get_alerts(user_id)
        return alerts

    def create_alert(self, entity: CreateAlert, user_id: str):
        alert_id = self._alert_repository.create_alert(entity, user_id)
        return alert_id

    def update_alert(self, entity: CreateAlert, alert_id: str):
        alert_id = self._alert_repository.update_alert(entity, alert_id)
        return alert_id

    def delete_alert(self, alert_id: str):
        alert_id = self._alert_repository.delete_alert(alert_id)
        return alert_id
