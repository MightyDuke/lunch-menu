from bs4 import BeautifulSoup
from .base import ScrapingProvider, Menu

class ToniProvider(ScrapingProvider):
    name = "Toni"
    homepage = "https://www.restauracetoni.cz"
    fetch_url = "https://www.restauracetoni.cz/"

    async def construct_menu(self, site: BeautifulSoup, menu: Menu):
        for element in site.find_all(class_ = "menublok"):
            date = self.parse_date(element.find(class_ = "denmenu").text)
            day = menu.create_day(date)
            
            for i, item in enumerate(element.find_all(class_ = "menu-post-content")):
                content = self.find_strings(item)
                name = self.clean_name(content[0], i == 0)
                price = self.parse_price(content[1])

                day.add_item(name, price)