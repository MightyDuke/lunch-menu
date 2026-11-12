from typing import Annotated
from fastapi import Depends
from datetime import date, datetime
from fastapi_singleton import singleton
from lunch_menu.services.redis_client import RedisClientService
from lunch_menu.services.user import UserService

@singleton
class VotingService:
    vote_expiration = 604_800

    def __init__(
        self, 
        redis_client: Annotated[RedisClientService, Depends(RedisClientService)], 
        user_service: Annotated[UserService, Depends(UserService)]
    ):
        self.redis_client = redis_client
        self.session_service = user_service

    async def get_votes(self, *, target_date: str | None = None):
        result = {}
        votes, users = await self.redis_client.hgetallm("votes", "users")

        if target_date is not None:
            result[target_date] = {}

        for key in sorted(votes.keys(), key = votes.get):
            date, establishment, user_id = key.split(":")

            if target_date is not None and date != target_date:
                continue

            if date not in result:
                result[date] = {}

            if establishment not in result[date]:
                result[date][establishment] = []

            if user_id in users:
                result[date][establishment].append({"id": user_id, **users[user_id]})

        return result

    async def vote(self, user_id: str, date: date, establishment: str):
        field = f"{date}:{establishment}:{user_id}"
        vote_exists = await self.redis_client.hdel("votes", field)

        if not vote_exists:
            now = datetime.now().isoformat()
            await self.redis_client.hset("votes", field, now, expiration = self.vote_expiration)

        votes = await self.get_votes(target_date = str(date))
        await self.redis_client.publish("votes", votes)

    async def listen(self):
        votes = await self.get_votes()
        yield votes

        async for votes in self.redis_client.subscribe("votes"):
            yield votes