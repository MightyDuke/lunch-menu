import re
from bs4 import BeautifulSoup
from . import Menu, ScrapingProvider, parse_date, parse_price

def clean_name(text: str):
    text = text.strip()

    if "zdarma" in text.lower():
        if match := re.match(r"(.*)\s*\(", text):
            text = match.group(1).strip()

    return text

class PaletaProvider(ScrapingProvider):
    name = "Paleta"
    homepage = "https://www.paletarestaurant.cz"
    fetch_url = "https://www.paletarestaurant.cz/menu/menu.php"

    async def fetch_menu(self, site: BeautifulSoup, menu: Menu):
        for element in site.body.find_all("h3"):
            date = parse_date(element.text)
            day = menu.create_day(date)

            for item in element.find_next_sibling("table").find_all("tr"):
                name = clean_name(item.find(class_ = "meal-name").text)
                price = parse_price(item.find(class_ = "meal-price").text)

                day.add_item(name, price)