from bs4 import BeautifulSoup
from lunch_menu.establishments.base import WebScraperEstablishment, Menu, clean_name, parse_date, parse_price, find_strings

class ToniEstablishment(WebScraperEstablishment):
    name = "Toni"
    homepage = "https://www.restauracetoni.cz"
    fetch_url = "https://www.restauracetoni.cz/"

    def process_site(self, site: BeautifulSoup, menu: Menu):
        for element in site.find_all(class_ = "menublok"):
            date = parse_date(element.find(class_ = "denmenu").text)
            
            for i, item in enumerate(element.find_all(class_ = "menu-post-content")):
                content = find_strings(item)
                name = clean_name(content[0], is_soup = i == 0)
                price = parse_price(content[1])

                menu.add_item(date, name, price)