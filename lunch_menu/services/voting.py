from typing import Annotated
from fastapi import Depends
from lunch_menu.services.redis_client import RedisClientService
from lunch_menu.services.session import SessionService

class VotingService:
    def __init__(self, redis_client: Annotated[RedisClientService, Depends()], session_service: Annotated[SessionService, Depends()]):
        self.redis_client = redis_client
        self.session_service = session_service

    async def _get_votes(self):
        result = {}
        votes = await self.redis_client.hgetall("votes")
        users = await self.redis_client.hgetall("users")

        for key, value in votes.items():
            if value not in result:
                result[value] = []

            if key in users:
                result[value].append(users[key])

        return result

    async def vote(self, id: str, path: str):
        await self.redis_client.hset("votes", id, path, expiration = 604_800)
        votes = await self._get_votes()

        await self.redis_client.publish("votes", votes)


    async def listen(self):
        votes = await self._get_votes()

        yield votes

        async for votes in self.redis_client.subscribe("votes"):
            yield votes