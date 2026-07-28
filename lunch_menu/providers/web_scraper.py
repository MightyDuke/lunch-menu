from aiocache import Cache
from aiocache.lock import RedLock
from httpx import AsyncClient
from bs4 import BeautifulSoup
from .base import Provider, Menu

class WebScraperProvider(Provider):
    fetch_url: str
    link_only: bool = False

    def __init__(self, *, client: AsyncClient, cache: Cache, expiration: int, **kwargs):
        super().__init__(**kwargs)

        self.client = client
        self.cache = cache
        self.expiration = expiration

    @property
    def cache_key(self):
        return f"lunch_menu:establishment:{self.key}"

    async def get_menu(self) -> Menu:
        result = await self.cache.get(self.cache_key)

        if result is None:
            async with RedLock(self.cache, self.cache_key, lease = 3.0):
                result = await self.cache.get(self.cache_key)

                if result is None:
                    self.logger.info(f"{self.key}: fetch {self.fetch_url}")
                    response = await self.client.get(self.fetch_url)

                    site = BeautifulSoup(response.text, features = "lxml")
                    menu = Menu()

                    self.process_site(site, menu)
                    result = menu.serialize()

                    await self.cache.set(self.cache_key, result, ttl = self.expiration)

        return result

    def process_site(self, site: BeautifulSoup, menu: Menu):
        raise NotImplementedError()