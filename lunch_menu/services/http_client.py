from typing import Annotated
from logging import getLogger
from fastapi import Depends
from bs4 import BeautifulSoup
from httpx import AsyncClient
from lunch_menu.models.settings import Settings, get_settings

logger = getLogger("uvicorn.error")

class HttpClientService:
    def __init__(self, settings: Annotated[Settings, Depends(get_settings)]):
        headers = {}

        if settings.user_agent is not None:
            headers["User-agent"] = settings.user_agent

        self.timeout = settings.timeout
        self.client = AsyncClient(http2 = True, timeout = self.timeout, headers = headers)

    async def fetch(self, url: str) -> BeautifulSoup:
        async with self.client:
            logger.info(f"fetch {url}")

            response = await self.client.get(url)
            soup = BeautifulSoup(response.text, features = "lxml")

        return soup