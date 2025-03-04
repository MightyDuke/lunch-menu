from . import Provider

class HodonankaProvider(Provider):
    name = "Hodoňanka"
    url = "https://www.rozvoz-jidla-ostrava.cz"

    async def get_menu(self):
        return "https://www.rozvoz-jidla-ostrava.cz/clanky/jidelni-listek"