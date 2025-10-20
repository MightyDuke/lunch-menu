from cashews import Cache
from httpx import AsyncClient
from sanic.exceptions import NotFound, BadRequest
from sanic.log import logger
from lunch_menu import establishments
from asyncio import CancelledError

class LunchMenuService:
    establishments = {
        "boasi": establishments.BoasiEstablishment,
        "paleta": establishments.PaletaEstablishment,
        "blesk": establishments.BleskEstablishment, 
        "hodonanka": establishments.HodonankaEstablishment,
        "pastaafidli": establishments.PastaFidliEstablishment,
        "mbrestaurace": establishments.MBRestauraceEstablishment,
        "phobo": establishments.PhoboEstablishment,
        "tajmahal": establishments.TajMahalEstablishment
    }

    def __init__(self, *, cache_url: str = "disk://", expiration: str = "10m"):
        self.client = AsyncClient()
        self.cache = Cache()

        self.cache.setup(cache_url)

        self.instances = {
            key: cls(key = key, client = self.client, cache = self.cache, expiration = expiration) 
            for key, cls 
            in self.establishments.items()
        }

    async def get_establishments(self):
        return {
            key: {
                "name": instance.name,
                "homepage": instance.homepage,
                "linkOnly": instance.link_only
            }
            for key, instance
            in self.instances.items()
        }

    async def get_menu(self, establishment: str):
        instance = self.instances.get(establishment)

        if instance is None:
            raise NotFound(f"Establishment \"{establishment}\" not found")

        try:
            result = await instance.get_menu()
        except NotImplementedError:
            raise BadRequest(f"Establishment \"{establishment}\" doesn't provide a menu")
        except CancelledError:
            result = {}
        except:
            logger.exception(f"{instance.__class__.__name__}, {establishment} - get_menu")
            result = {}

        return result