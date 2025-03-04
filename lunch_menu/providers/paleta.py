from . import Menu, Provider, parse_date, parse_price, parse_name

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
                price = parse_price(item.find(class_ = "meal-price").text)
                name = item.find(class_ = "meal-name").text

                if price is None:
                    name = name.replace("( polévka k menu ZDARMA )", "")

                name = parse_name(name, price)

                day.add_item(name, price)

        return menu.serialize()