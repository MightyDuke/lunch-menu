import json
from contextlib import asynccontextmanager
from typing import Any
from fastapi import Request
from redis.asyncio import ConnectionPool, Redis

serialize = lambda value: json.dumps(value)
deserialize = lambda value: json.loads(value)

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
            value = deserialize(value)

        return value

    async def set(self, key: str, value: Any, *, expiration: int = None):
        value = serialize(value)

        await self.client.set(key, value, ex = expiration)
    
    async def hget(self, key: str, field: str, *, expiration: int = None) -> Any | None:
        if expiration is None:
            value = await self.client.hget(key, field)
        else:
            value = await self.client.hgetex(key, field, ex = expiration)
            value = value[0]

        if value is not None:
            value = deserialize(value)

        return value

    async def hset(self, key: str, field: str, value: Any, *, expiration: int = None):
        value = serialize(value)

        if expiration is None:
            await self.client.hset(key, field, value)
        else:
            await self.client.hsetex(key, field, value, ex = expiration)

    async def hgetall(self, key: str) -> Any:
        value = await self.client.hgetall(key)
        result = {}

        if value is not None:
            for key in value.keys():
                result[key.decode()] = deserialize(value[key])

        return result

    async def hgetallm(self, *keys: str) -> list[Any]:
        async with self.client.pipeline() as pipeline:
            for key in keys:
                await pipeline.hgetall(key)

            values = await pipeline.execute()

        result = []

        for value in values:
            if value is not None:
                item = {}

                for key in value.keys():
                    item[key.decode()] = deserialize(value[key])

                result.append(item)
            else:
                result.append(None)

        return result

    async def delete(self, key: str) -> int:
        return await self.client.delete(key)

    async def hgetdel(self, key: str, field: str) -> Any | None:
        value = await self.client.hgetdel(key, field)
        value = value[0]

        if value is not None:
            value = deserialize(value)

        return value

    async def publish(self, channel: str, message: Any):
        message = serialize(message)

        await self.client.publish(channel, message)

    def lock(self, key: str, *, timeout: int = 60):
        return self.client.lock(f"{key}:lock", timeout = timeout)

    async def subscribe(self, channel: str):
        async with self.client.pubsub(ignore_subscribe_messages = True) as pubsub:
            await pubsub.subscribe(channel)

            async for message in pubsub.listen():
                yield deserialize(message["data"])

    @asynccontextmanager
    async def pipeline(self):
        async with self.client.pipeline() as pipeline:
            instance = RedisClientService(self.request, client = pipeline)
            yield instance
            await pipeline.execute()