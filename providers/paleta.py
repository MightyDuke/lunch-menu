from bs4 import BeautifulSoup
from .base import ScrapingProvider, Menu

class PaletaProvider(ScrapingProvider):
    name = "Paleta"
    homepage = "https://www.paletarestaurant.cz"
    fetch_url = "https://www.paletarestaurant.cz/menu/menu.php"

    async def construct_menu(self, site: BeautifulSoup, menu: Menu):
        for element in site.body.find_all("h3"):
            date = self.parse_date(element.text)
            day = menu.create_day(date)

            for item in element.find_next_sibling("table").find_all("tr"):
                name = self.clean_name(item.find(class_ = "meal-name").text)
                price = self.parse_price(item.find(class_ = "meal-price").text)

                day.add_item(name, price)