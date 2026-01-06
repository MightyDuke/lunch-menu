from bs4 import BeautifulSoup
from lunch_menu.base import WebScraperEstablishment, Menu
from lunch_menu.helpers import clean_name, parse_date, parse_price

class HodonankaEstablishment(WebScraperEstablishment):
    name = "Hodoňanka"
    homepage = "https://www.rozvoz-jidla-ostrava.cz"
    fetch_url = "https://www.menicka.cz/api/iframe/?id=1545"

    def process_site(self, site: BeautifulSoup, menu: Menu):
        for element in site.body.find_all(class_ = "content"):
            date = parse_date(element.find("h2").contents[0].text)

            if date.weekday() in (5, 6):
                continue

            for item in element.find_all(class_ = "photomenu"):
                name = clean_name(item.find(class_ = "food").text, is_soup = "soup" in item.attrs["class"], suffix_removal_count = 1)
                price = parse_price(item.find(class_ = "prize").text)

                menu.add_item(date, name, price)
