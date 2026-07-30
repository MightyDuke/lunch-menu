from bs4 import BeautifulSoup
from lunch_menu.providers.base import AddMenuItemCallback
from lunch_menu.providers.web_scraper import WebScraperProvider
from lunch_menu.providers.helpers import clean_name, parse_date, parse_price

class MBRestauraceEstablishment(WebScraperProvider):
    name = "MB Restaurace"
    homepage = "https://mbrestaurace.cz"
    fetch_url = "https://mbrestaurace.cz/restaurace"

    def process_site(self, site: BeautifulSoup, add_item: AddMenuItemCallback):
        menu_element = site.body.find(id = "dennimenu")
        date_element = menu_element.select_one(":scope > div > div:nth-child(3)")

        date = parse_date(date_element.text)

        menu_elements = menu_element.select(":scope > div > div:nth-child(4) > div > div > div > div")

        for item in menu_elements:
            name = item.select_one(":scope > div > div > div > div:nth-child(1)").text

            name = clean_name(name.replace("k menu ZDARMA", ""))
            price = parse_price(item.select_one(":scope > div > div > div > div:nth-child(2)").text)

            if name == "": 
                continue

            add_item(date, name, price)
