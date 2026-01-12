from asyncio import CancelledError
from aiocache import Cache
from httpx import AsyncClient
from sanic import Config
from sanic.exceptions import NotFound, BadRequest
from sanic.log import logger
from lunch_menu import establishments

class LunchMenuService:
    establishments = {
        "bo-asi": establishments.BoasiEstablishment,
        "paleta": establishments.PaletaEstablishment,
        "blesk": establishments.BleskEstablishment, 
        "hodonanka": establishments.HodonankaEstablishment,
        "pasta-a-fidli": establishments.PastaFidliEstablishment,
        "mb-restaurace": establishments.MBRestauraceEstablishment,
        "delphi": establishments.DelphiEstablishment,
        "u-zlateho-jarouse": establishments.UZlatehoJarouseEstablishment,
        "toni": establishments.ToniEstablishment,
        "phobo": establishments.PhoboEstablishment,
        "taj-mahal": establishments.TajMahalEstablishment
    }

    def __init__(self, config: Config):
        cache_url = config.get("CACHE_URL", "memory://")
        expiration = config.get("CACHE_EXPIRATION", "600")
        user_agent = config.get("CRAWLER_USER_AGENT", None)

        headers = {}

        if user_agent is not None:
            headers["User-Agent"] = user_agent

        self.client = AsyncClient(http2 = True, headers = headers)
        self.cache = Cache.from_url(cache_url)

        self.instances = {
            key: cls(key = key, client = self.client, cache = self.cache, expiration = int(expiration)) 
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
