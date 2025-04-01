import re
from . import Menu, Provider, parse_date, parse_price

def clean_name(text: str):
    text = text.strip()

    if "zdarma" in text.lower():
        if match := re.match(r"(.*)\s*\(", text):
            text = match.group(1).strip()

    return text

class PaletaProvider(Provider):
    name = "Paleta"
    url = "https://www.paletarestaurant.cz"

    async def get_menu(self):
        menu = Menu()
        soup = await self.fetch("https://www.paletarestaurant.cz/menu/menu.php")

        for element in soup.body.find_all("h3"):
            date = parse_date(element.text)
            day = menu.create_day(date)

            for item in element.find_next_sibling("table").find_all("tr"):
                name = clean_name(item.find(class_ = "meal-name").text)
                price = parse_price(item.find(class_ = "meal-price").text)

                day.add_item(name, price)

        return menu.serialize()