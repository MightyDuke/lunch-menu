from bs4 import BeautifulSoup
from lunch_menu.providers.base import AddMenuItemCallback
from lunch_menu.providers.web_scraper import WebScraperProvider
from lunch_menu.providers.helpers import clean_name, parse_date, parse_price

class MenickaCzProvider(WebScraperProvider): 
    id: int

    @property
    def url(self):
        return f"https://www.menicka.cz/api/iframe/?id={self.id}"

    def process_site(self, site: BeautifulSoup, add_item: AddMenuItemCallback):
        for element in site.body.find_all(class_ = "content"):
            date = parse_date(element.find("h2").contents[0].text)

            if date.weekday() in (5, 6):
                continue

            for item in element.find_all(class_ = "photomenu"):
                name = clean_name(item.find(class_ = "food").text.replace("\u200b", " "), prefix_removal_count = 1, suffix_removal_count = 1)
                price = parse_price(item.find(class_ = "prize").text)

                add_item(date, name, price)
