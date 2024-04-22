import json
from typing import Optional

from redis import Redis

from app.metrics.entities.ping_config import PingConfig
from app.database.repositories.ping_config.interface import IPingConfigRepository


class PingConfigRedisRepository(IPingConfigRepository):
    def __init__(self, redis_client: Redis) -> None:
        self._redis = redis_client

    def get(self, ping_id: str) -> Optional[PingConfig]:
        serialized = self._redis.get(ping_id)

        if not serialized:
            return None

        raw_ping_config = json.loads(serialized)

        return PingConfig(**raw_ping_config)

    def save(self, entity: PingConfig) -> None:
        serialized = json.dumps(entity.to_dict())

        self._redis.set(entity.id, serialized)

    def delete(self, ping_id: str) -> None:
        self._redis.delete(ping_id)
