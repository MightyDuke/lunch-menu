from providers.toni import ToniProvider
from providers.boasi import BoasiProvider
from providers.paleta import PaletaProvider
from providers.blesk import BleskProvider
from providers.phobo import PhoboProvider
from providers.hodonanka import HodonankaProvider
from providers.pastafidli import PastaFidliProvider

class LunchMenuService:
    providers = {
        "toni": ToniProvider,
        "boasi": BoasiProvider,
        "paleta": PaletaProvider,
        "blesk": BleskProvider, 
        "hodonanka": HodonankaProvider,
        "pastaafidli": PastaFidliProvider,
        "phobo": PhoboProvider,
    }

    def __init__(self):
        self.instances = {key: cls() for key, cls in self.providers.items()}

    async def get_providers(self):
        return list(self.providers.keys())

    async def get_menu(self, provider: str):
        instance = self.instances[provider]
        result = await instance.get_menu()

        return {
            "name": instance.name,
            "homepage": instance.homepage,
            "menu": result
        }
