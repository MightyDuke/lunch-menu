from cashews import cache
from httpx import AsyncClient
from bs4 import BeautifulSoup
from sanic.log import logger
from common.menu import Menu

client = AsyncClient(http2 = True)

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

    def __init__(self, *, key: str, **kwargs):
        super().__init__(**kwargs)
        self.key = key

    @cache(ttl = "10m", key = "lunch_menu:{self.key}", lock = True)
    async def get_menu(self) -> Menu:
        logger.info(f"Fetching {self.fetch_url}")

        try:
            response = await client.get(self.fetch_url)
            site = BeautifulSoup(response.text, features = "html.parser")
            menu = Menu()

            self.process_site(site, menu)

            result = menu.serialize()
        except:
            raise RuntimeError(self.key)

        return result

    def process_site(self, site: BeautifulSoup, menu: Menu):
        pass