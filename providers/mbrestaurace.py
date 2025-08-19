from bs4 import BeautifulSoup
from common.provider import WebProvider
from common.menu import Menu
from common.utils import clean_name, parse_date, parse_price

class MBRestauraceProvider(WebProvider):
    name = "MB Restaurace"
    homepage = "https://mbrestaurace.cz"
    fetch_url = "https://mbrestaurace.cz/restaurace"

    def process_site(self, site: BeautifulSoup, menu: Menu):
        menu_element = site.body.find(id = "dennimenu")
        date_element = menu_element.select_one(":scope > div > div:nth-child(3)")

        date = parse_date(date_element.text)
        day = menu.create_day(date)

        menu_elements = menu_element.select(":scope > div > div:nth-child(4) > div > div > div > div")

        for item in menu_elements:
            name = item.select_one(":scope > div > div > div > div:nth-child(1)").text

            name = clean_name(name.replace("k menu", ""))
            price = parse_price(item.select_one(":scope > div > div > div > div:nth-child(2)").text)

            if name == "": 
                continue

            day.add_item(name, price)

    