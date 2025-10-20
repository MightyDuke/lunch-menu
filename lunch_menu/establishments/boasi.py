from bs4 import BeautifulSoup
from lunch_menu.establishment import WebScraperEstablishment
from lunch_menu.menu import Menu
from lunch_menu.utils import clean_name, parse_date, parse_price

class BoasiEstablishment(WebScraperEstablishment):
    name = "Bo Asi!"
    homepage = "https://www.boasi.cz"
    fetch_url = "https://www.paletarestaurant.cz/menu-boasi/menu.php"

    def process_site(self, site: BeautifulSoup, menu: Menu):
        for element in site.body.find_all("h2"):
            date = parse_date(element.text)
            day = menu.create_day(date)

            for item in element.find_next_sibling("table").find_all("tr"):
                name = clean_name(item.find(class_ = "food").text)
                price = parse_price(item.find(class_ = "prize").text)

                day.add_item(name, price)