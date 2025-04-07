from bs4 import BeautifulSoup
from .base import ScrapingProvider, Menu

class PastaFidliProvider(ScrapingProvider):
    name = "Pasta & Fidli"
    homepage = "https://www.pastaafidli.cz"
    fetch_url = "https://www.pastaafidli.cz/cz/denni-menu/"

    async def construct_menu(self, site: BeautifulSoup, menu: Menu):
        for element in site.body.find_all(class_ = "day"):
            date = self.parse_date(element.find("td").text)
            day = menu.create_day(date)

            if date is not None and date.weekday() in (5, 6):
                continue

            sibling = element

            while sibling := sibling.find_next_sibling():
                if not sibling.has_attr("class"):
                    continue

                if sibling.name != "tr" or sibling.has_attr("class") and "day" in sibling.attrs["class"] or "shift" in sibling.attrs["class"]:
                    break

                name = self.clean_name(sibling.find("td").text)
                price = self.parse_price(sibling.find(class_ = "price").text)

                day.add_item(name, price)