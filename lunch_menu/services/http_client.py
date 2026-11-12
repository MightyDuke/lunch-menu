from typing import Annotated
from fastapi import Depends
from bs4 import BeautifulSoup
from fastapi_singleton import singleton
from httpx import AsyncClient
from lunch_menu.models.settings import Settings, get_settings
from lunch_menu.services.logger import LoggerService

@singleton
class HttpClientService:
    def __init__(
        self, 
        settings: Annotated[Settings, Depends(get_settings)],
        logger: Annotated[LoggerService, Depends(LoggerService)]
    ):
        self.settings = settings
        self.timeout = self.settings.http_timeout
        self.logger = logger

    def create_client(self):
        headers = {}

        if self.settings.user_agent is not None:
            headers["User-agent"] = self.settings.user_agent

        return AsyncClient(http2 = True, timeout = self.timeout, headers = headers)

    async def fetch(self, url: str) -> BeautifulSoup:
        client = self.create_client()

        async with client:
            self.logger.info(f"fetch {url}")

            response = await client.get(url)
            soup = BeautifulSoup(response.text, features = "lxml")

        return soup