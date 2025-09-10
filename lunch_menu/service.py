from cashews import Cache
from httpx import AsyncClient, TimeoutException
from sanic.exceptions import NotFound, BadRequest
from sanic.log import logger
from lunch_menu import providers
from asyncio import CancelledError

class LunchMenuService:
    providers = {
        "toni": providers.ToniProvider,
        "boasi": providers.BoasiProvider,
        "paleta": providers.PaletaProvider,
        "blesk": providers.BleskProvider, 
        "hodonanka": providers.HodonankaProvider,
        "pastaafidli": providers.PastaFidliProvider,
        "mbrestaurace": providers.MBRestauraceProvider,
        "phobo": providers.PhoboProvider
    }

    def __init__(self, *, cache_url: str = "disk://", expiration: str = "10m"):
        self.client = AsyncClient()
        self.cache = Cache()

        self.cache.setup(cache_url)

        self.instances = {
            key: cls(key = key, client = self.client, cache = self.cache, expiration = expiration) 
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
        except CancelledError:
            result = {}
        except:
            logger.exception(f"{instance.__class__.__name__}, {provider} - get_menu")
            result = {}

        return result