from bs4 import BeautifulSoup
from lunch_menu.establishments.base import WebScraperEstablishment, Menu, clean_name, parse_date, parse_price

class PaletaEstablishment(WebScraperEstablishment):
    name = "Paleta"
    homepage = "https://www.paletarestaurant.cz"
    fetch_url = "https://www.paletarestaurant.cz/menu/menu.php"

    def process_site(self, site: BeautifulSoup, menu: Menu):
        for element in site.body.find_all("h3"):
            date = parse_date(element.text)

            for item in element.find_next_sibling("table").find_all("tr"):
                name = clean_name(item.find(class_ = "meal-name").text)
                price = parse_price(item.find(class_ = "meal-price").text)

                menu.add_item(date, name, price)