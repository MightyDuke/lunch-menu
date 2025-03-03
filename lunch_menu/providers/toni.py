from . import Menu, Provider, find_strings, parse_date, parse_price

class ToniProvider(Provider):
    name = "Toni"
    url = "https://www.restauracetoni.cz"

    async def generate_menu(self):
        menu = Menu()
        soup = await self.fetch("https://www.restauracetoni.cz/")

        for element in soup.find_all(class_ = "menublok"):
            date = parse_date(element.find(class_ = "denmenu").text)
            day = menu.create_day(date)
            
            for i, item in enumerate(element.find_all(class_ = "menu-post-content")):
                content = find_strings(item)

                day.add_item(
                    content[0].strip() if i > 0 else f"Polévka {content[0][0].lower() + content[0][1:]}",
                    parse_price(content[1])
                )

        return menu