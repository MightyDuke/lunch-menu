from bs4 import BeautifulSoup
from lunch_menu.establishment import WebScraperEstablishment
from lunch_menu.menu import Menu
from lunch_menu.utils import clean_name, parse_date, parse_price, find_strings

class ToniEstablishment(WebScraperEstablishment):
    name = "Toni"
    homepage = "https://www.restauracetoni.cz"
    fetch_url = "https://www.restauracetoni.cz/"

    def process_site(self, site: BeautifulSoup, menu: Menu):
        for element in site.find_all(class_ = "menublok"):
            date = parse_date(element.find(class_ = "denmenu").text)
            day = menu.create_day(date)
            
            for i, item in enumerate(element.find_all(class_ = "menu-post-content")):
                content = find_strings(item)
                name = clean_name(content[0], i == 0)
                price = parse_price(content[1])

                day.add_item(name, price)