from . import Menu, Provider, parse_date, parse_price
import re

def clean_name(text: str):
    text = text.strip()

    if match := re.match(r"(?:\d+\.\s*)?(.*)", text):
        text = match.group(1).strip()

    if match := re.match(r"(.*)\s*\(", text):
        text = match.group(1).strip()

    return text

class BleskProvider(Provider):
    name = "Hasičárna Blesk"
    url = "https://www.hasicarnableskostrava.cz"

    async def get_menu(self):
        menu = Menu()
        soup = await self.fetch("https://www.hasicarnableskostrava.cz/poledni-menu")

        for element in soup.body.find_all(class_ = "food-section"):
            date = parse_date(element.text)
            day = menu.create_day(date)

            sibling = element

            while (sibling := sibling.find_next_sibling()) and sibling.name == "div":
                name = clean_name(sibling.find("h3").text)
                price = parse_price(sibling.find("span").text)

                day.add_item(name, price)

        return menu.serialize()