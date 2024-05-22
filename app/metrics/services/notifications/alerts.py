from app.database.repositories import AlertRepository
from app.metrics.entities import PingConfig
from app.metrics.services.notifications.notifier import EmailNotifier
from app.routes.serializers import CreateAlert
from app.metrics.entities.alert import Alert as AlertEntity


class AlertsService:
    def __init__(self, alert_repository: AlertRepository, notifier: EmailNotifier) -> None:
        self._alert_repository = alert_repository
        self._notifier = notifier

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

    def send_alert(self, ping_config: PingConfig, alert_entity: AlertEntity):
        try:
            subject = f'HOST UNAVAILABLE {ping_config.host}'
            body = f'ICMP ping for {ping_config.host} has failed. Please, review service'

            self._notifier.send_email(subject, body, alert_entity.email)
        except Exception as e:
            print('FAILED EMAIL SEND', e)
