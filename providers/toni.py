from bs4 import BeautifulSoup
from . import Menu, ScrapingProvider, find_strings, parse_date, parse_price

def clean_name(text: str, is_soup: bool):
    text = text.strip()

    if "polévka" not in text.lower() and is_soup:
        text = f"Polévka {text[0].lower()}{text[1:]}"

    return text

class ToniProvider(ScrapingProvider):
    name = "Toni"
    homepage = "https://www.restauracetoni.cz"
    fetch_url = "https://www.restauracetoni.cz/"

    async def fetch_menu(self, site: BeautifulSoup, menu: Menu):
        for element in site.find_all(class_ = "menublok"):
            date = parse_date(element.find(class_ = "denmenu").text)
            day = menu.create_day(date)
            
            for i, item in enumerate(element.find_all(class_ = "menu-post-content")):
                content = find_strings(item)
                name = clean_name(content[0], i == 0)
                price = parse_price(content[1])

                day.add_item(name, price)