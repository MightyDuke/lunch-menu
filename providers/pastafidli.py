from . import Menu, Provider, parse_date, parse_price
import re

def clean_name(text: str):
    text = text.strip()

    if match := re.match(r"(?:\d+\.)?(.*)\s*\(.*\) \(", text):
        text = match.group(1).strip()

    return text

class PastaFidliProvider(Provider):
    name = "Pasta & Fidli"
    url = "https://www.pastaafidli.cz"

    async def get_menu(self):
        menu = Menu()
        soup = await self.fetch("https://www.pastaafidli.cz/cz/denni-menu/")

        for element in soup.body.find_all(class_ = "day"):
            date = parse_date(element.find("td").text)
            day = menu.create_day(date)

            if date is not None and date.weekday() in (5, 6):
                continue

            sibling = element

            while sibling := sibling.find_next_sibling():
                if not sibling.has_attr("class"):
                    continue

                if sibling.name != "tr" or sibling.has_attr("class") and "day" in sibling.attrs["class"] or "shift" in sibling.attrs["class"]:
                    break

                name = clean_name(sibling.find("td").text)
                price = parse_price(sibling.find(class_ = "price").text)

                day.add_item(name, price)

        return menu.serialize()