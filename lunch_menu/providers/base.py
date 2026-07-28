from typing import Literal
from logging import getLogger
from datetime import date

class Menu:
    def __init__(self):
        self.menu = {}
    
    def add_item(self, when: date | Literal["week"], name: str, price: int = None):
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
            elif when is None or when != "week":
                when = "week"
            else:
                when = str(when)

            result[when] = items

        return result

class Provider:
    name: str = None
    homepage: str = None
    link_only: bool = True

    def __init__(self, *, key: str, **kwargs):
        self.key = key
        self.logger = getLogger(f"establishments.{self.key}")

    async def get_menu(self) -> Menu:
        raise NotImplementedError()