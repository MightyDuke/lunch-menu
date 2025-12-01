import re
import dateparser
from cashews import Cache
from httpx import AsyncClient
from bs4 import BeautifulSoup
from sanic.log import logger
from bs4 import BeautifulSoup
from datetime import date

def clean_name(text: str, is_soup: bool = False, *, suffix_removal_count: int = 1):
    text = text.strip()

    if match := re.match(r"(?:\d+\.\s*)?(.*)", text):
        text = match.group(1).strip()

    for _ in range(suffix_removal_count):
        if match := re.match(r"(.*)\(.+\)\*?$", text):
            text = match.group(1).strip()

    if is_soup:
        text = f"Polévka {text[0].lower()}{text[1:]}"

    return text

def parse_date(text: str) -> date:
    result = dateparser.parse(text, languages = ["cs"]) 
    return result.date() if result else None

def parse_price(text: str) -> int:
    if match := re.match(r"(\d+)", text):
        return int(match.group(1))

def find_strings(soup: BeautifulSoup):
    return [
        string.text.strip()
        for string
        in soup.find_all(string = True)
        if not str.isspace(string)
    ]

class Menu:
    def __init__(self):
        self.menu = {}
    
    def add_item(self, when: date | str, name: str, price: int = None):
        if when not in self.menu:
            self.menu[when] = []

        self.menu[when].append({
            "name": name,
            "price": price
        })
    
    def serialize(self):
        result = {}

        for when, items in self.menu.items():
            if isinstance(when, date):
                when = when.isoformat()
            elif when is None:
                when = "week"
            else:
                when = str(when)

            result[when] = items

        return result

class Establishment:
    name: str = None
    homepage: str = None
    link_only: bool = True

    def __init__(self, **kwargs):
        pass

    async def get_menu(self) -> Menu:
        raise NotImplementedError()

class WebScraperEstablishment(Establishment):
    fetch_url: str
    link_only: bool = False

    def __init__(self, *, key: str, client: AsyncClient, cache: Cache, expiration: str, **kwargs):
        self.key = key
        self.client = client
        self.cache = cache
        self.expiration = expiration

    @property
    def cache_key(self):
        return f"lunch_menu:establishment:{self.key}"

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
        raise NotImplementedError()