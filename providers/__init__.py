import logging
import dateparser
import re
from pathlib import Path
from tempfile import gettempdir
from datetime import date
from diskcache import Cache
from httpx import AsyncClient
from bs4 import BeautifulSoup

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

class Day:
    def __init__(self):
        self.items = []

    def add_item(self, name: str, price: int):
        self.items.append((name, price))

class Menu:
    def __init__(self):
        self.menu = {}

    def create_day(self, when: date):
        day = Day()
        self.menu[when] = day

        return day
    
    def serialize(self):
        return {
            when if when else "week": [
                { 
                    "name": name, 
                    "price": price 
                }
                for name, price
                in days.items
            ]
            for when, days
            in self.menu.items()
            if len(days.items) > 0
        }

class Provider:
    name: str = None
    homepage: str = None

    async def get_menu(self):
        pass

class ScrapingProvider(Provider):
    fetch_url: str

    client = AsyncClient()
    cache = Cache(Path(gettempdir()) / "lunch_menu_cache")
    expire = 600

    @property
    def class_name(self):
        return self.__class__.__name__

    async def get_menu(self):
        result = self.cache.get(self.class_name)

        if result is None:
            try:
                response = (await self.client.get(self.fetch_url)).text
                soup = BeautifulSoup(response, features = "html.parser")
                menu = Menu()

                await self.fetch_menu(soup, menu)
                result = menu.serialize()
            except:
                logging.exception(self.class_name)
                result = None
                
            if result is not None:
                self.cache.set(self.class_name, result, expire = self.expire)

        return result

    async def fetch_menu(self, soup: BeautifulSoup, menu: Menu):
        pass