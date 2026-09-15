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

    def get_fetch_url(self):
        return self.fetch_url

    async def get_menu(self) -> dict:
        cache_key = f"establishment:{self.key}"
        menu = await self.redis_client.get(cache_key)

        if menu is None:
            async with self.redis_client.lock(cache_key, timeout = self.http_client.timeout):
                menu = await self.redis_client.get(cache_key)

                if menu is None:
                    fetch_url = self.get_fetch_url()
                    site = await self.http_client.fetch(fetch_url)

                    menu, add_menu_item_callback = self.create_menu()
                    self.process_site(site, add_menu_item_callback)

                    await self.redis_client.set(cache_key, menu, expiration = self.expiration)

        return menu

    def process_site(self, site: BeautifulSoup, add_item: AddMenuItemCallback):
        raise NotImplementedError()