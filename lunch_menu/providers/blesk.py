from bs4 import BeautifulSoup
from lunch_menu.provider import WebProvider
from lunch_menu.menu import Menu
from lunch_menu.utils import clean_name, parse_date, parse_price

class BleskProvider(WebProvider):
    name = "Hasičárna Blesk"
    homepage = "https://www.hasicarnableskostrava.cz"
    fetch_url = "https://www.hasicarnableskostrava.cz/poledni-menu"

    def process_site(self, site: BeautifulSoup, menu: Menu):
        for element in site.body.find_all(class_ = "food-section"):
            date = parse_date(element.text)
            day = menu.create_day(date)

            sibling = element
            is_soup = True

            while (sibling := sibling.find_next_sibling()) and sibling.name == "div":
                name = clean_name(sibling.find("h3").text, is_soup)
                price = parse_price(sibling.find("span").text)
                is_soup = False

                day.add_item(name, price)