from bs4 import BeautifulSoup
from .base import ScrapingProvider, Menu

class MBRestauraceProvider(ScrapingProvider):
    name = "MB Restaurace"
    homepage = "https://mbrestaurace.cz"
    fetch_url = "https://mbrestaurace.cz/restaurace"

    async def construct_menu(self, site: BeautifulSoup, menu: Menu):
        menu_element = site.body.find(id = "dennimenu")
        date_element = menu_element.select_one(":scope > div > div:nth-child(3)")

        date = self.parse_date(date_element.text)
        day = menu.create_day(date)

        menu_elements = menu_element.select(":scope > div > div:nth-child(4) > div > div > div > div")

        for item in menu_elements:
            name = item.select_one(":scope > div > div > div > div:nth-child(1)").text

            name = self.clean_name(name.replace("k menu", ""))
            price = self.parse_price(item.select_one(":scope > div > div > div > div:nth-child(2)").text)

            day.add_item(name, price)

    