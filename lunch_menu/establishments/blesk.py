from bs4 import BeautifulSoup
from lunch_menu.establishments.base import WebScraperEstablishment, Menu, clean_name, parse_date, parse_price

class BleskEstablishment(WebScraperEstablishment):
    name = "Hasičárna Blesk"
    homepage = "https://www.hasicarnableskostrava.cz"
    fetch_url = "https://www.hasicarnableskostrava.cz/poledni-menu"

    def process_site(self, site: BeautifulSoup, menu: Menu):
        for element in site.body.find_all(class_ = "food-section"):
            date = parse_date(element.text)

            sibling = element
            is_soup = True

            while (sibling := sibling.find_next_sibling()) and sibling.name == "div":
                name = clean_name(sibling.find("h3").text, is_soup)
                price = parse_price(sibling.find("span").text)
                is_soup = False

                menu.add_item(date, name, price)