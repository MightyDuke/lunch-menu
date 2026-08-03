from bs4 import BeautifulSoup
from lunch_menu.providers.base import AddMenuItemCallback
from lunch_menu.providers.web_scraper import WebScraperProvider
from lunch_menu.providers.helpers import clean_name, parse_date, parse_price

class PastaFidliEstablishment(WebScraperProvider):
    name = "Pasta & Fidli"
    homepage = "https://www.pastaafidli.cz"
    fetch_url = "https://www.pastaafidli.cz/cz/denni-menu/"

    def process_site(self, site: BeautifulSoup, add_item: AddMenuItemCallback):
        for element in site.body.find_all(class_ = "day"):
            date = parse_date(element.find("td").text)

            if date is not None and date.weekday() in (5, 6):
                continue

            sibling = element

            while sibling := sibling.find_next_sibling():
                if not sibling.has_attr("class"):
                    continue

                if sibling.name != "tr" or sibling.has_attr("class") and "day" in sibling.attrs["class"] or "shift" in sibling.attrs["class"]:
                    break

                name = clean_name(sibling.find("td").text, suffix_removal_count = 2)
                price = parse_price(sibling.find(class_ = "price").text)

                add_item(date, name, price)
