from bs4 import BeautifulSoup
from lunch_menu.establishments.base import WebScraperEstablishment, Menu, clean_name, parse_date, parse_price

class UZlatehoJarouseEstablishment(WebScraperEstablishment):
    name = "Koliba u zlatého Jarouše"
    homepage = "https://uzlatehojarouse.cz/"
    fetch_url = "https://www.menicka.cz/api/iframe/?id=1502"

    def process_site(self, site: BeautifulSoup, menu: Menu):
        for element in site.body.find_all(class_ = "content"):
            date = parse_date(element.find("h2").contents[0].text)

            if date.weekday() in (5, 6):
                continue

            for item in element.find_all("tr"):
                name = clean_name(item.find(class_ = "food").text, is_soup = "soup" in item.attrs["class"], prefix_removal_count = 1)
                price = parse_price(item.find(class_ = "prize").text)

                menu.add_item(date, name, price)