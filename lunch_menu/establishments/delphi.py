from bs4 import BeautifulSoup
from lunch_menu.establishments.base import WebScraperEstablishment, Menu, clean_name, parse_date, parse_price

class DelphiEstablishment(WebScraperEstablishment):
    name = "Delphi"
    homepage = "https://restaurantdelphi.cz/delphi-i/"
    fetch_url = "https://restaurantdelphi.cz/delphi-i/"

    def process_site(self, site: BeautifulSoup, menu: Menu):
        for element in site.find_all(class_ = "daily-menu"):
            date = element.find("strong").text.strip()[2:]
            date = parse_date(date)

            for item in element.find_all("li"):
                subitems = item.find_all("span")

                if not subitems:
                    name = clean_name(item.text, is_soup = True)
                    menu.add_item(date, name)
                else:
                    name = clean_name(subitems[0].text)
                    price = parse_price(subitems[2].text)

                    menu.add_item(date, name, price)