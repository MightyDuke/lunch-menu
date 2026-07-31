import json
from contextlib import asynccontextmanager
from typing import Any
from fastapi import Request
from redis.asyncio import ConnectionPool, Redis

class RedisClientService:
    @staticmethod
    def create_connection_pool(url: str):
        return ConnectionPool.from_url(url)

    def __init__(self, request: Request, *, client = None):
        self.request = request
        self.client = Redis(connection_pool = request.app.state.redis_pool) if client is None else client

    async def get(self, key: str, *, expiration: int = None) -> Any:
        if expiration is None:
            value = await self.client.get(key)
        else:
            value = await self.client.getex(key, ex = expiration)

        if value is not None:
            value = json.loads(value)

        return value

    async def set(self, key: str, value: Any, *, expiration: int = None):
        value = json.dumps(value)

        await self.client.set(key, value, ex = expiration)
    
    async def hget(self, key: str, field: str) -> Any | None:
        value = await self.client.hget(key, field)

        if value is not None:
            value = json.loads(value)

        return value

    async def hset(self, key: str, field: str, value: Any, *, expiration: int = None):
        value = json.dumps(value)

        if expiration is None:
            await self.client.hset(key, field, value)
        else:
            await self.client.hsetex(key, field, value, ex = expiration)

    async def delete(self, key: str) -> int:
        return await self.client.delete(key)

    def lock(self, key: str):
        return self.client.lock(f"{key}:lock")

    @asynccontextmanager
    async def pipeline(self):
        async with self.client.pipeline() as pipeline:
            instance = RedisClientService(self.request, client = pipeline)
            yield instance
            await pipeline.execute()