import dateparser
import re
from datetime import date
from httpx import AsyncClient
from bs4 import BeautifulSoup
from diskcache import Cache
from tempfile import gettempdir
from pathlib import Path

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
            when: [
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
    client = AsyncClient()
    cache = Cache(Path(gettempdir()) / "lunch_menu_cache")

    def __init__(self, expire: int = 600):
        self.expire = expire

    @property
    def class_name(self):
        return self.__class__.__name__

    async def get_menu(self):
        result = await self.generate_menu()

        if isinstance(result, Menu):
            return result.serialize()
        else:
            return result

    async def generate_menu(self, menu: Menu):
        pass

    async def fetch(self, url: str) -> BeautifulSoup:
        self.cache.expire()

        if item := self.cache.get(self.class_name):
            response = item
        else:
            response = (await self.client.get(url)).text
            self.cache.add(self.class_name, response, expire = self.expire)

        return BeautifulSoup(response, features = "html.parser")
    
