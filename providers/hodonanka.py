from . import Provider, Menu, parse_date, parse_price
import re

def clean_name(text: str, is_soup: str):
    text = text.strip()

    if match := re.match(r"(?:\d+\.\s*)?(.*)", text):
        text = match.group(1).strip()

    if match := re.match(r"(.*)\s*\(", text):
        text = match.group(1).strip()

    if is_soup:
        text = f"Polévka {text[0].lower()}{text[1:]}"

    return text

class HodonankaProvider(Provider):
    name = "Hodoňanka"
    url = "https://www.rozvoz-jidla-ostrava.cz"

    async def get_menu(self):
        menu = Menu()
        site = await self.fetch("https://www.menicka.cz/1545-hodonanka.html")

        for element in site.find_all(class_ = "menicka"):
            date = parse_date(element.find(class_ = "nadpis").text)
            day = menu.create_day(date)

            if element := element.find(class_ = "popup-gallery"):
                for item in element.find_all("li"):
                    price = parse_price(item.find(class_ = "cena").text)
                    name = clean_name(item.find(class_ = "polozka").text, price < 100)

                    day.add_item(name, price)

        return menu.serialize()