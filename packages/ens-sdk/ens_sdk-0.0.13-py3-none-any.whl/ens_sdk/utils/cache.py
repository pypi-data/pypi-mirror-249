import redis
from pydantic.typing import Optional


class Cache:

    def __init__(self):
        self._cache = redis.Redis()

    def store(self, key: str, value: str):
        self._set(key, value)

    def _set(self, key: str, value: str) -> None:
        self._cache.set(key, value)

    def _get(self, key: str) -> Optional[str]:
        value = self._cache.get(key)
        return value.decode("utf-8") if value else None

    def retrieve(self, key: str) -> Optional[str]:
        return self._get(key)



