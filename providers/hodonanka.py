from bs4 import BeautifulSoup
from common.provider import WebProvider
from common.menu import Menu
from common.utils import clean_name, parse_date, parse_price

class HodonankaProvider(WebProvider):
    name = "Hodoňanka"
    homepage = "https://www.rozvoz-jidla-ostrava.cz"
    fetch_url = "https://www.menicka.cz/1545-hodonanka.html"

    def process_site(self, site: BeautifulSoup, menu: Menu):
        for element in site.find_all(class_ = "menicka"):
            date = parse_date(element.find(class_ = "nadpis").text)
            day = menu.create_day(date)

            if element := element.find(class_ = "popup-gallery"):
                for item in element.find_all("li"):
                    price = parse_price(item.find(class_ = "cena").text)
                    name = clean_name(item.find(class_ = "polozka").text, price < 100)

                    day.add_item(name, price)