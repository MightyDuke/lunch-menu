from typing import Annotated, TypedDict
from secrets import token_urlsafe
from hashlib import shake_256
from base64 import urlsafe_b64encode
from fastapi import Depends, HTTPException, Request
from fastapi import status
from federatedidentity import Issuer, verify_id_token
from federatedidentity.exceptions import InvalidClaimsError
from lunch_menu.models.settings import Settings, get_settings
from lunch_menu.services.redis_client import RedisClientService

def hash_user_id(iss: str, sub: str, *, digest_length: int = 30):
    digest = shake_256(f"{iss}:{sub}".encode()).digest(digest_length)
    return urlsafe_b64encode(digest).decode()

class User(TypedDict):
    name: str
    picture: str | None

class UserService:
    user_profile_expiration = 2_628_000

    @staticmethod
    async def discover_issuers(allowed_issuers: list[str]) -> dict[str, Issuer]:
        result = {}

        for issuer_url in allowed_issuers:
            issuer = await Issuer.async_from_discovery(issuer_url)
            result[issuer_url] = issuer

        return result

    def __init__(self, request: Request, redis_client: Annotated[RedisClientService, Depends()], settings: Annotated[Settings, Depends(get_settings)]):
        self.issuers = request.app.state.issuers
        self.redis_client = redis_client

        self.valid_audiences = settings.oauth2_clients.values()
        self.session_expiration = settings.session_expiration

    async def create_session(self, id_token: str) -> str:
        try:
            claims = verify_id_token(id_token, valid_issuers = self.issuers, valid_audiences = self.valid_audiences)
        except InvalidClaimsError:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Failed to validate id token")

        user_id = hash_user_id(claims["iss"], claims["sub"])
        user = User(
            name = claims["name"] if "name" in claims else "???",
            picture = claims["picture"] if "picture" in claims else None
        )

        token = token_urlsafe(30)

        async with self.redis_client.pipeline() as pipeline:
            await pipeline.set(f"session:{token}", user_id, expiration = self.session_expiration)
            await pipeline.hset("users", user_id, user, expiration = self.user_profile_expiration)

        return token

    async def get_session(self, token: str) -> str | None:
        user_id = await self.redis_client.get(f"session:{token}", expiration = self.session_expiration)

        if user_id is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid session token")

        return user_id

    async def get_user(self, token: str) -> User | None:
        user_id = await self.get_session(token)

        if user_id is None:
            return

        return await self.redis_client.hget("users", user_id, expiration = self.user_profile_expiration)

    async def delete_session(self, token: str):
        await self.redis_client.delete(f"session:{token}")