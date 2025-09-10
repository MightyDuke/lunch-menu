from cashews import Cache
from httpx import AsyncClient
from bs4 import BeautifulSoup
from sanic.log import logger
from lunch_menu.menu import Menu

class Provider:
    name: str = None
    homepage: str = None
    link_only: bool = True

    def __init__(self, **kwargs):
        pass

    async def get_menu(self) -> Menu:
        raise NotImplementedError()

class WebProvider(Provider):
    fetch_url: str
    link_only: bool = False

    def __init__(self, *, key: str, client: AsyncClient, cache: Cache, expiration: str, **kwargs):
        self.key = key
        self.client = client
        self.cache = cache
        self.expiration = expiration

    @property
    def cache_key(self):
        return f"lunch_menu:provider:{self.key}"

    async def get_menu(self) -> Menu:
        async with self.cache.lock(f"{self.cache_key}:lock", 5.0):
            result = await self.cache.get(self.cache_key)

            if result is None:
                logger.info(f"{self.key}: fetch {self.fetch_url}")
                response = await self.client.get(self.fetch_url)

                site = BeautifulSoup(response.text, features = "html.parser")
                menu = Menu()

                self.process_site(site, menu)
                result = menu.serialize()

                await self.cache.set(self.cache_key, result, expire = self.expiration)

            return result

    def process_site(self, site: BeautifulSoup, menu: Menu):
        pass