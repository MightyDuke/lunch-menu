from providers.blesk import BleskProvider
from providers.toni import ToniProvider
from providers.boasi import BoasiProvider
from providers.paleta import PaletaProvider
from providers.hodonanka import HodonankaProvider
from providers.pastafidli import PastaFidliProvider
from providers.mbrestaurace import MBRestauraceProvider
from providers.phobo import PhoboProvider
from sanic.exceptions import NotFound, BadRequest
from sanic.log import logger

class LunchMenuService:
    providers = {
        "toni": ToniProvider,
        "boasi": BoasiProvider,
        "paleta": PaletaProvider,
        "blesk": BleskProvider, 
        "hodonanka": HodonankaProvider,
        "pastaafidli": PastaFidliProvider,
        "mbrestaurace": MBRestauraceProvider,
        "phobo": PhoboProvider,
    }

    def __init__(self):
        self.instances = {
            key: cls(key = key) 
            for key, cls 
            in self.providers.items()
        }

    async def get_providers(self):
        return {
            key: {
                "name": instance.name,
                "homepage": instance.homepage,
                "linkOnly": instance.link_only
            }
            for key, instance
            in self.instances.items()
        }

    async def get_menu(self, provider: str):
        instance = self.instances.get(provider)

        if instance is None:
            raise NotFound(f"Provider \"{provider}\" not found")

        try:
            result = await instance.get_menu()
        except NotImplementedError:
            raise BadRequest(f"Provider \"{provider}\" doesn't provide a menu")
        except:
            logger.exception(instance.__class__.__name__)
            result = {}

        return result