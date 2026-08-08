from bs4 import BeautifulSoup
from lunch_menu.services.http_client import HttpClientService
from lunch_menu.services.redis_client import RedisClientService
from lunch_menu.providers.base import AddMenuItemCallback, MenuProvider

class WebScraperProvider(MenuProvider):
    fetch_url: str

    def __init__(self, *, http_client: HttpClientService, redis_client: RedisClientService, expiration: int, **kwargs):
        super().__init__(**kwargs)

        self.http_client = http_client
        self.redis_client = redis_client
        self.expiration = expiration

    @property
    def url(self):
        return self.fetch_url

    @property
    def cache_key(self):
        return f"establishment:{self.key}"

    async def get_menu(self) -> dict:
        menu = await self.redis_client.get(self.cache_key)

        if menu is None:
            async with self.redis_client.lock(self.cache_key, timeout = self.http_client.timeout + 5):
                menu = await self.redis_client.get(self.cache_key)

                if menu is None:
                    site = await self.http_client.fetch(self.url)

                    menu, add_menu_item_callback = self.create_menu()
                    self.process_site(site, add_menu_item_callback)

                    await self.redis_client.set(self.cache_key, menu, expiration = self.expiration)

        return menu

    def process_site(self, site: BeautifulSoup, menu: AddMenuItemCallback):
        raise NotImplementedError()