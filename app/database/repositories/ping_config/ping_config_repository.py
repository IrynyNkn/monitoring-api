from typing import Optional, List, Dict, Any

from sqlalchemy.orm import Session

from app.metrics.entities.ping_config import PingConfig
from app.database.repositories.ping_config.interface import IPingConfigRepository
from app.database.tables import IcmpPingConfig as IcmpPingConfigTable


class PingConfigRepository(IPingConfigRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, ping_id: str) -> Optional[PingConfig]:
        entity = self._session.query(IcmpPingConfigTable).get(ping_id)

        if not entity:
            return None

        return PingConfig(
            id=str(entity.id),
            host=entity.hostname,
            interval=entity.check_interval,
            owner_id=entity.user_id,
            status="active"  # placeholder
        )

    def save(self, entity: PingConfig) -> str:
        db_entity = IcmpPingConfigTable(
            user_id=entity.owner_id,
            hostname=entity.host,
            check_interval=entity.interval,
            is_paused=False
        )

        self._session.add(db_entity)
        self._session.commit()

        return str(db_entity.id)

    def delete(self, ping_id: str) -> Optional[str]:
        ping_to_delete = self._session.query(IcmpPingConfigTable).get(ping_id)

        if ping_to_delete:
            self._session.delete(ping_to_delete)
            self._session.commit()
            return ping_id

        return None

    def get_pings_by_user_id(self, user_id: str) -> List[Dict[str, Any]]:
        pings = self._session.query(IcmpPingConfigTable).filter(IcmpPingConfigTable.user_id == user_id).all()

        result: List[Dict[str, Any]] = []
        for p in pings:
            result.append(PingConfig(
                id=str(p.id),
                host=p.hostname,
                interval=p.check_interval,
                status="active"  # placeholder
            ).to_dict())

        return result

