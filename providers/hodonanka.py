from bs4 import BeautifulSoup
from .base import ScrapingProvider, Menu

class HodonankaProvider(ScrapingProvider):
    name = "Hodoňanka"
    homepage = "https://www.rozvoz-jidla-ostrava.cz"
    fetch_url = "https://www.menicka.cz/1545-hodonanka.html"

    async def construct_menu(self, site: BeautifulSoup, menu: Menu):
        for element in site.find_all(class_ = "menicka"):
            date = self.parse_date(element.find(class_ = "nadpis").text)
            day = menu.create_day(date)

            if element := element.find(class_ = "popup-gallery"):
                for item in element.find_all("li"):
                    price = self.parse_price(item.find(class_ = "cena").text)
                    name = self.clean_name(item.find(class_ = "polozka").text, price < 100)

                    day.add_item(name, price)