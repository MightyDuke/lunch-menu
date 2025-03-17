from . import Menu, Provider, parse_date, parse_price

def clean_name(text: str):
    return text.strip()

class BoasiProvider(Provider):
    name = "Bo Asi!"
    url = "https://www.boasi.cz"

    async def get_menu(self):
        menu = Menu()
        soup = await self.fetch("https://www.paletarestaurant.cz/menu-boasi/menu.php")

        for element in soup.body.find_all("h2"):
            date = parse_date(element.text)
            day = menu.create_day(date)

            for item in element.find_next_sibling("table").find_all("tr"):
                name = clean_name(item.find(class_ = "food").text)
                price = parse_price(item.find(class_ = "prize").text)

                day.add_item(name, price)

        return menu.serialize()