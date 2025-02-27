from . import Menu, Provider, parse_date, parse_price

class PaletaProvider(Provider):
    name = "Paleta"
    url = "https://www.paletarestaurant.cz"

    async def generate_menu(self, menu: Menu):
        soup = await self.fetch("https://www.paletarestaurant.cz/menu/menu.php")

        for element in soup.body.find_all("h3"):
            date = parse_date(element.text)
            day = menu.create_day(date)

            for i, item in enumerate(element.find_next_sibling("table").find_all("tr")):
                name = item.find(class_ = "meal-name").text
                price = item.find(class_ = "meal-price").text

                if i == 0:
                    name = name.replace("( polévka k menu ZDARMA )", "")

                day.add_item(
                    name.strip(),
                    parse_price(price) if price else None
                )