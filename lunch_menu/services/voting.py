from typing import Annotated
from fastapi import Depends
from datetime import date
from lunch_menu.services.redis_client import RedisClientService
from lunch_menu.services.user import UserService

class VotingService:
    def __init__(self, redis_client: Annotated[RedisClientService, Depends()], session_service: Annotated[UserService, Depends()]):
        self.redis_client = redis_client
        self.session_service = session_service

    async def get_votes(self, *, target_date: str = None):
        result = {}
        votes, users = await self.redis_client.hgetallm("votes", "users")

        if target_date is not None:
            result[target_date] = {}

        for key, path in votes.items():
            date, id = key.split(":", maxsplit = 1)

            if target_date is not None and date != target_date:
                continue

            if date not in result:
                result[date] = {}

            if path not in result[date]:
                result[date][path] = []

            if id in users:
                result[date][path].append(users[id])

        return result

    async def vote(self, id: str, date: date, path: str):
        field = f"{date}:{id}"
        vote = await self.redis_client.hgetdel("votes", field)

        if vote != path:
            await self.redis_client.hset("votes", field, path, expiration = 604_800)

        votes = await self.get_votes(target_date = str(date))
        await self.redis_client.publish("votes", votes)

    async def listen(self):
        votes = await self.get_votes()
        yield votes

        async for votes in self.redis_client.subscribe("votes"):
            yield votes