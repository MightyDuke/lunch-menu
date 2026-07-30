from bs4 import BeautifulSoup
from lunch_menu.providers.base import AddMenuItemCallback
from lunch_menu.providers.web_scraper import WebScraperProvider
from lunch_menu.providers.helpers import clean_name, parse_date, parse_price

class BleskEstablishment(WebScraperProvider):
    name = "Hasičárna Blesk"
    homepage = "https://www.hasicarnableskostrava.cz"
    fetch_url = "https://www.hasicarnableskostrava.cz/poledni-menu"

    def process_site(self, site: BeautifulSoup, add_item: AddMenuItemCallback):
        for element in site.body.find_all(class_ = "food-section"):
            date = parse_date(element.text)

            sibling = element
            is_soup = True

            while (sibling := sibling.find_next_sibling()) and sibling.name == "div":
                name = sibling.find("h3").text

                if date and is_soup:
                    name = name.removesuffix("v ceně menu")
                    name += ")"

                name = clean_name(name, remove_numbering = True, suffix_removal_count = 1)
                price = parse_price(sibling.find("span").text)
                is_soup = False

                add_item(date, name, price)