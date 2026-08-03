from typing import Callable, Literal
from datetime import date

AddMenuItemCallback = Callable[[date | Literal["week"] | str, str, int], None]

class Provider:
    name: str = None
    homepage: str = None
    link_only: bool = True

    def __init__(self, *, key: str, **kwargs):
        self.key = key

    async def get_menu(self) -> dict:
        raise NotImplementedError()

class MenuProvider(Provider):
    link_only: bool = False

    def __init__(self, *, highlighted_words: list[str], **kwargs):
        super().__init__(**kwargs)

        self.highlighted_words = highlighted_words

    def create_menu(self) -> tuple[dict, AddMenuItemCallback]:
        menu = {}

        def add_menu_item_callback(when: date | Literal["week"] | str, name: str, price: int = None):
            if isinstance(when, date):
                when = when.isoformat()
            elif when is None or when != "week":
                when = "week"

            if when not in menu:
                menu[when] = []

            menu[when].append({
                "name": name,
                "price": price,
                "highlight": any(word.lower() in name.lower() for word in self.highlighted_words)
            })

        return (menu, add_menu_item_callback)
