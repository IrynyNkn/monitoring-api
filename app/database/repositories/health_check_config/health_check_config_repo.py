from typing import Optional, List, Dict, Any

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.metrics.entities import HealthCheckConfig
from app.database.repositories.health_check_config.interface import IHealthCheckConfigRepository
from app.database.tables import HttpPingConfig as HttpPingConfigTable


class HealthCheckConfigRepo(IHealthCheckConfigRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, health_check_id: str) -> Optional[HealthCheckConfig]:
        entity = self._session.query(HttpPingConfigTable).get(health_check_id)

        if not entity:
            return None

        return HealthCheckConfig(
            id=str(entity.id),
            endpoint_url=entity.endpoint_url,
            interval=entity.check_interval,
        )

    def save(self, entity: HealthCheckConfig) -> str:
        db_entity = HttpPingConfigTable(
            user_id=entity.owner_id,
            endpoint_url=entity.endpoint_url,
            check_interval=entity.interval,
            is_paused=False
        )

        self._session.add(db_entity)
        self._session.commit()

        return str(db_entity.id)

    def delete(self, health_check_id: str) -> None:
        try:
            deletion_health_check = self._session.query(HttpPingConfigTable).get(health_check_id)
            if deletion_health_check:
                self._session.delete(deletion_health_check)
                self._session.commit()
                return deletion_health_check
        except SQLAlchemyError:
            self._session.rollback()
        finally:
            self._session.close()

        return None

    def update_health_check(self, health_check_id: str, interval: int) -> Optional[str]:
        try:
            old_ping = self._session.query(HttpPingConfigTable).get(health_check_id)
            if old_ping:
                old_ping.check_interval = int(interval)
            self._session.commit()
            return str(old_ping.id)
        except SQLAlchemyError as e:
            print(f"An error occurred in update_health_check: {e}")
            self._session.rollback()
        finally:
            self._session.close()

    def get_health_checks_by_user_id(self, user_id: str) -> List[Dict[str, Any]]:
        health_checks = self._session.query(HttpPingConfigTable).filter(HttpPingConfigTable.user_id == user_id).all()

        result: List[Dict[str, Any]] = []
        for hc in health_checks:
            result.append(HealthCheckConfig(
                id=str(hc.id),
                endpoint_url=hc.endpoint_url,
                interval=hc.check_interval,
                created_at=hc.created_at
            ).to_dict())

        return result
