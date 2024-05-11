from typing import List, Dict, Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database.repositories.alerts.interface import IAlertsRepository
from app.metrics.entities.alert import Alert as AlertEntity
from app.routes.serializers import CreateAlert
from app.database.tables import Alert as AlertTable


class AlertRepository(IAlertsRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create_alert(self, entity: CreateAlert, user_id: str) -> str:
        db_entity = AlertTable(
            user_id=user_id,
            email=entity.email,
            for_=entity.for_,
            repeat_alert=entity.repeat_alert,
            alert_group=entity.alert_group,
            alert_type=entity.alert_type
        )

        self._session.add(db_entity)
        self._session.commit()

        return str(db_entity.id)

    def get_alerts(self, user_id: str):
        alerts = self._session.query(AlertTable).filter(AlertTable.user_id == user_id).all()

        result: List[Dict[str, Any]] = []
        for alert in alerts:
            result.append(AlertEntity(
                id=str(alert.id),
                email=alert.email,
                for_=alert.for_,
                repeat_alert=alert.repeat_alert,
                alert_group=alert.alert_group,
                alert_type=alert.alert_type
            ).to_dict())

        return result

    def update_alert(self, entity: CreateAlert, alert_id: str):
        try:
            old_alert = self._session.query(AlertTable).get(alert_id)
            if old_alert:
                old_alert.email = entity.email
                old_alert.for_ = entity.for_
                old_alert.repeat_alert = entity.repeat_alert
                old_alert.alert_group = entity.alert_group
                old_alert.alert_type = entity.alert_type
            self._session.commit()
            return str(old_alert.id)
        except SQLAlchemyError as e:
            print(f"An error occurred: {e}")
            self._session.rollback()
        finally:
            self._session.close()

        return None

    def delete_alert(self, alert_id: str):
        try:
            alert_to_delete = self._session.query(AlertTable).get(alert_id)
            if alert_to_delete:
                self._session.delete(alert_to_delete)
                self._session.commit()
                return alert_id
        except SQLAlchemyError:
            self._session.rollback()
        finally:
            self._session.close()

        return None
