from bs4 import BeautifulSoup
from lunch_menu.providers.base import AddMenuItemCallback
from lunch_menu.providers.web_scraper import WebScraperProvider
from lunch_menu.providers.helpers import clean_name, parse_date, parse_price

class DelphiEstablishment(WebScraperProvider):
    name = "Delphi"
    homepage = "https://restaurantdelphi.cz/delphi-i/"
    fetch_url = "https://restaurantdelphi.cz/delphi-i/"

    def process_site(self, site: BeautifulSoup, add_item: AddMenuItemCallback):
        for element in site.find_all(class_ = "daily-menu"):
            date = element.find("strong").text.strip()[2:]
            date = parse_date(date)

            for item in element.find_all("li"):
                subitems = item.find_all("span")

                if not subitems:
                    name = clean_name(item.text)
                    price = None
                else:
                    name = clean_name(subitems[0].text)
                    price = parse_price(subitems[2].text)

                add_item(date, name, price)
