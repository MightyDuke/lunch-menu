from bs4 import BeautifulSoup
from .base import ScrapingProvider, Menu

class BleskProvider(ScrapingProvider):
    name = "Hasičárna Blesk"
    homepage = "https://www.hasicarnableskostrava.cz"
    fetch_url = "https://www.hasicarnableskostrava.cz/poledni-menu"

    async def construct_menu(self, site: BeautifulSoup, menu: Menu):
        for element in site.body.find_all(class_ = "food-section"):
            date = self.parse_date(element.text)
            day = menu.create_day(date)

            sibling = element
            is_soup = True

            while (sibling := sibling.find_next_sibling()) and sibling.name == "div":
                name = self.clean_name(sibling.find("h3").text, is_soup)
                price = self.parse_price(sibling.find("span").text)
                is_soup = False

                day.add_item(name, price)