from . import Menu, Provider, parse_date, parse_price, parse_name
import re

class PastaFidliProvider(Provider):
    name = "Pasta & Fidli"
    url = "https://www.pastaafidli.cz"

    async def get_menu(self):
        menu = Menu()
        soup = await self.fetch("https://www.pastaafidli.cz/cz/denni-menu/")

        for element in soup.body.find_all(class_ = "day"):
            date = parse_date(element.find("td").text)
            day = menu.create_day(date)

            if date is None:
                continue

            if date.weekday in (5, 6):
                break

            sibling = element

            while sibling := sibling.find_next_sibling():
                if not sibling.has_attr("class"):
                    continue

                if sibling.name != "tr" or sibling.has_attr("class") and "day" in sibling.attrs["class"]:
                    break

                price = parse_price(sibling.find(class_ = "price").text)
                name = parse_name(sibling.find("td").text, price)

                if match := re.match(r"(?:\d+\.)?(.*)\s*\(.*\) \(", name):
                    name = match.group(1).strip()

                day.add_item(name, price)

        return menu.serialize()