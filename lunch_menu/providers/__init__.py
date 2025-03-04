import re
import dateparser
from datetime import date
from httpx import AsyncClient
from bs4 import BeautifulSoup

SOUP_PRICE_THRESHOLD = 100

def parse_date(text: str) -> date:
    result = dateparser.parse(text, languages = ["cs"]) 
    return result.date() if result else None

def parse_price(text: str) -> int:
    if match := re.match(r"(\d+)", text):
        return int(match.group(1))

def parse_name(text: str, price: int) -> str:
    text = text.strip()

    if (price is None or price < SOUP_PRICE_THRESHOLD) and "polévka" not in text.lower():
        text = f"Polévka {text[0].lower() + text[1:]}"

    return text

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

    name: str = None
    url: str = None

    @property
    def class_name(self):
        return self.__class__.__name__

    async def get_menu(self, menu: Menu):
        pass

    async def fetch(self, url: str) -> BeautifulSoup:
        response = (await self.client.get(url)).text
        return BeautifulSoup(response, features = "html.parser")
    
