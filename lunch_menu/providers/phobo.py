from . import Provider

class PhoboProvider(Provider):
    name = "Pho Bo"
    url = "https://www.facebook.com/p/PHO-BO-Restaurant-100082901603735"

    async def generate_menu(self):
        return "https://www.facebook.com/p/PHO-BO-Restaurant-100082901603735"

