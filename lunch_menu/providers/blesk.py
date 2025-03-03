from . import Menu, Provider, parse_date, parse_price, parse_name
import re

class BleskProvider(Provider):
    name = "Hasičárna Blesk"
    url = "https://www.hasicarnableskostrava.cz"

    async def generate_menu(self):
        menu = Menu()
        soup = await self.fetch("https://www.hasicarnableskostrava.cz/poledni-menu")

        for element in soup.body.find_all(class_ = "food-section"):
            date = parse_date(element.text)
            day = menu.create_day(date)

            if date is None:
                continue

            sibling = element

            while (sibling := sibling.find_next_sibling()) and sibling.name == "div":
                price = parse_price(sibling.find("span").text)
                name = parse_name(sibling.find("h3").text, price)

                if match := re.match(r"(?:\d+\.)?(.*)\s*\(", name):
                    name = match.group(1).strip()

                day.add_item(name, price)

        return menu