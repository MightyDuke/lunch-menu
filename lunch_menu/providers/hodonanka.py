from . import Provider

class HodonankaProvider(Provider):
    name = "Hodoňanka"
    url = "https://www.rozvoz-jidla-ostrava.cz"

    async def generate_menu(self):
        return "https://www.rozvoz-jidla-ostrava.cz/clanky/jidelni-listek"