import providers

class LunchMenuService:
    providers = {
        "toni": providers.ToniProvider,
        "boasi": providers.BoasiProvider,
        "paleta": providers.PaletaProvider,
        "blesk": providers.BleskProvider, 
        "hodonanka": providers.HodonankaProvider,
        "pastaafidli": providers.PastaFidliProvider,
        "phobo": providers.PhoboProvider,
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
