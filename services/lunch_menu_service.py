import providers

class LunchMenuService:
    providers = {
        "toni": providers.ToniProvider,
        "boasi": providers.BoasiProvider,
        "paleta": providers.PaletaProvider,
        "blesk": providers.BleskProvider, 
        "hodonanka": providers.HodonankaProvider,
        "pastaafidli": providers.PastaFidliProvider,
        "mbrestaurace": providers.MBRestauraceProvider,
        "phobo": providers.PhoboProvider,
    }

    def __init__(self, *, expire: int = 600):
        self.instances = {key: cls(expire = expire) for key, cls in self.providers.items()}

    async def get_providers(self):
        return [
            {
                "name": key,
                "title": instance.name,
                "homepage": instance.homepage
            }
            for key, instance
            in self.instances.items()
        ]

    async def get_menu(self, provider: str):
        instance = self.instances[provider]
        result = await instance.get_menu()

        return {
            "menu": result
        }
