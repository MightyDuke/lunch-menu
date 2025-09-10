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

    def __init__(self, *, key: str, client: AsyncClient, cache: Cache, expiration: str, soft_expiration: str, **kwargs):
        self.key = key
        self.client = client
        self.cache = cache
        self.expiration = expiration

        self.get_menu = self.cache.early(self.expiration, early_ttl = soft_expiration, key = f"lunch_menu:provider:{self.key}")(self.get_menu)

    async def get_menu(self) -> Menu:
        logger.info(f"{self.key}: fetch {self.fetch_url}")
        response = await self.client.get(self.fetch_url)

        site = BeautifulSoup(response.text, features = "html.parser")
        menu = Menu()

        self.process_site(site, menu)
        return menu.serialize()

    def process_site(self, site: BeautifulSoup, menu: Menu):
        pass