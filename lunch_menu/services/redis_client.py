import json
from typing import Type, TypeVar
from fastapi import Request
from redis.asyncio import ConnectionPool, Redis
from pydantic import BaseModel

T = TypeVar("PydanticModel", bound = BaseModel)

class RedisClientService:
    prefix = "lunch_menu"

    @staticmethod
    def create_connection_pool(url: str):
        return ConnectionPool.from_url(url)

    @classmethod
    def prefixed_key(cls, key: str):
        return f"{cls.prefix}:{key}"

    def __init__(self, request: Request):
        self.client = Redis(connection_pool = request.app.state.redis_pool, decode_responses = True)

    async def set(self, key: str, value: BaseModel, *, expiration: int = None) -> None:
        await self.client.set(self.prefixed_key(key), value.model_dump_json(), ex = expiration)

    async def set_s(self, key: str, value: str, *, expiration: int = None) -> None:
        await self.client.set(self.prefixed_key(key), json.dumps(value), ex = expiration)
    
    async def get(self, cls: Type[T], key: str, *, expiration: int = None) -> T | None:
        if expiration is None:
            value = await self.client.get(self.prefixed_key(key))
        else:
            value = await self.client.getex(self.prefixed_key(key), ex = expiration)

        if value is not None:
            return cls.model_validate_json(value)

    async def get_s(self, key: str, *, expiration: int = None) -> str | None:
        if expiration is None:
            value = await self.client.get(self.prefixed_key(key))
        else:
            value = await self.client.getex(self.prefixed_key(key), ex = expiration)

        if value is not None:
            return json.loads(value)

    def lock(self, key: str):
        return self.client.lock(f"{key}:lock")