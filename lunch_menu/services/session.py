import secrets
from typing import Annotated, TypedDict
from fastapi import Depends, Request
from federatedidentity import Issuer, verify_id_token
from federatedidentity.transport import AsyncRequestBase, Response
from federatedidentity.exceptions import TransportError
from httpx import AsyncClient, RequestError
from lunch_menu.models.settings import Settings, get_settings
from lunch_menu.services.redis_client import RedisClientService

class HttpxTransport(AsyncRequestBase):
    async def __call__(self, url, body = None, method = None, headers = None) -> Response:
        async with AsyncClient(http2 = True) as client:
            try: 
                response = await client.get(url, headers = {"Accept": "application/json"})
            except RequestError as exception:
                raise TransportError(f"Error requesting URL {url!r}: {exception}")

            return Response( 
                content = response.content,
                status_code = response.status_code, 
                headers = response.headers
            ) 

class User(TypedDict):
    name: str
    picture: str | None

class SessionService:
    token_length = 32
    transport = HttpxTransport()

    @classmethod
    async def discover_issuers(cls, allowed_issuers: list[str]) -> dict[str, Issuer]:
        result = {}

        for issuer_url in allowed_issuers:
            issuer = await Issuer.async_from_discovery(issuer_url, request = cls.transport)
            result[issuer_url] = issuer

        return result

    def __init__(self, request: Request, redis_client: Annotated[RedisClientService, Depends()], settings: Annotated[Settings, Depends(get_settings)]):
        self.issuers = request.app.state.issuers
        self.redis_client = redis_client
        self.session_expiration = settings.session_expiration

    async def create_session(self, id_token: str) -> str:
        claims = verify_id_token(
            id_token, 
            valid_issuers = self.issuers.values(),
            valid_audiences = [
                "463687060136-hhf1has9o5c9q9nafcf62ruvueb5bbkj.apps.googleusercontent.com"
            ]
        )
        token = secrets.token_urlsafe(self.token_length)

        id = f"{claims["sub"]}@{claims["iss"]}"

        user = User(
            name = claims["name"] if "name" in claims else "???" ,
            picture = claims["picture"] if "picture" in claims else None
        )

        async with self.redis_client.pipeline() as pipeline:
            await pipeline.set(f"session:{token}", id, expiration = self.session_expiration)
            await pipeline.hset(f"users", id, user, expiration = 2_628_000)

        return token

    async def get_session(self, token: str) -> str | None:
        return await self.redis_client.get(f"session:{token}", expiration = self.session_expiration)

    async def get_user(self, token: str) -> User | None:
        id = await self.get_session(token)

        if id is None:
            return

        return await self.redis_client.hget("users", id)

    async def delete_session(self, token: str):
        await self.redis_client.delete(f"session:{token}")