import json
from typing import Annotated, Any
from fastapi import Depends
from fastapi_singleton import singleton
from redis.asyncio import Redis
from lunch_menu.models.settings import Settings, get_settings
from lunch_menu.services.logger import LoggerService

serialize = lambda value: json.dumps(value, ensure_ascii = False)
deserialize = lambda value: json.loads(value)

@singleton
class RedisClientService:
    def __init__(self, settings: Annotated[Settings, Depends(get_settings)], logger: Annotated[LoggerService, Depends(LoggerService)]):
        self.client =  Redis.from_url(settings.redis_url)
        logger.info(f"Using redis at \"{settings.redis_url}\"")

    async def get(self, key: str, *, expiration: int | None = None) -> Any:
        if expiration is None:
            value = await self.client.get(key)
        else:
            value = await self.client.getex(key, ex = expiration)

        if value is not None:
            value = deserialize(value)

        return value

    async def set(self, key: str, value: Any, *, expiration: int | None = None):
        value = serialize(value)

        await self.client.set(key, value, ex = expiration)
    
    async def hget(self, key: str, field: str, *, expiration: int | None = None) -> Any | None:
        if expiration is None:
            value = await self.client.hget(key, field)
        else:
            value = await self.client.hgetex(key, field, ex = expiration)
            value = value[0]

        if value is not None:
            value = deserialize(value)

        return value

    async def hset(self, key: str, field: str, value: Any, *, expiration: int | None = None):
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

    async def hgetallm(self, *keys: str) -> list[dict]:
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

    async def delete(self, key: str) -> bool:
        return await self.client.delete(key) > 0

    async def hdel(self, key: str, field: str) -> bool:
        value = await self.client.hdel(key, field)
        return value > 0

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