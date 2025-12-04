from cashews import Cache
from httpx import AsyncClient
from sanic.exceptions import NotFound, BadRequest
from sanic.log import logger
from asyncio import CancelledError
from lunch_menu.establishments.toni import ToniEstablishment
from lunch_menu.establishments.blesk import BleskEstablishment
from lunch_menu.establishments.boasi import BoasiEstablishment
from lunch_menu.establishments.paleta import PaletaEstablishment
from lunch_menu.establishments.hodonanka import HodonankaEstablishment
from lunch_menu.establishments.pastafidli import PastaFidliEstablishment
from lunch_menu.establishments.mbrestaurace import MBRestauraceEstablishment
from lunch_menu.establishments.delphi import DelphiEstablishment
from lunch_menu.establishments.phobo import PhoboEstablishment
from lunch_menu.establishments.tajmahal import TajMahalEstablishment

class LunchMenuService:
    establishments = {
        "boasi": BoasiEstablishment,
        "paleta": PaletaEstablishment,
        "blesk": BleskEstablishment, 
        "hodonanka": HodonankaEstablishment,
        "pastaafidli": PastaFidliEstablishment,
        "mbrestaurace": MBRestauraceEstablishment,
        "delphi": DelphiEstablishment,
        "toni": ToniEstablishment,
        "phobo": PhoboEstablishment,
        "tajmahal": TajMahalEstablishment
    }

    def __init__(self, *, cache_url: str = "disk://", expiration: str = "10m"):
        self.client = AsyncClient(http2 = True)
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