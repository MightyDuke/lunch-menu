import logging
import providers
from sanic.exceptions import NotFound

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
        self.instances = {
            key: cls(expire = expire) 
            for key, cls 
            in self.providers.items()
        }

    async def get_providers(self):
        return {
            key: {
                "name": instance.name,
                "homepage": instance.homepage
            }
            for key, instance
            in self.instances.items()
        }

    async def get_menu(self, provider: str):
        try:
            instance = self.instances[provider]
        except Exception as exception:
            raise NotFound(f"Provider \"{provider}\" not found") from exception

        try:
            result = await instance.get_menu()
        except:
            logging.exception(instance.__class__.__name__)
            result = {}

        return result