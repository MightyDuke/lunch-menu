from . import Menu, Provider, find_strings, parse_date, parse_price, parse_name

class ToniProvider(Provider):
    name = "Toni"
    url = "https://www.restauracetoni.cz"

    async def get_menu(self):
        menu = Menu()
        soup = await self.fetch("https://www.restauracetoni.cz/")

        for element in soup.find_all(class_ = "menublok"):
            date = parse_date(element.find(class_ = "denmenu").text)
            day = menu.create_day(date)
            
            for item in element.find_all(class_ = "menu-post-content"):
                content = find_strings(item)
                price = parse_price(content[1])
                name = parse_name(content[0], price)

                day.add_item(name, price)

        return menu.serialize()