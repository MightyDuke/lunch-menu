import logging
from diskcache import Cache
from tempfile import gettempdir
from pathlib import Path
from lunch_menu.providers.toni import ToniProvider
from lunch_menu.providers.boasi import BoasiProvider
from lunch_menu.providers.paleta import PaletaProvider
from lunch_menu.providers.blesk import BleskProvider
from lunch_menu.providers.phobo import PhoboProvider
from lunch_menu.providers.hodonanka import HodonankaProvider
from lunch_menu.providers.pastafidli import PastaFidliProvider

class LunchMenuService:
    providers = {
        "toni": ToniProvider,
        "boasi": BoasiProvider,
        "paleta": PaletaProvider,
        "blesk": BleskProvider, 
        "pastaafidli": PastaFidliProvider,
        "phobo": PhoboProvider,
        "hodonanka": HodonankaProvider,
    }

    def __init__(self, expire: int):
        self.instances = {key: cls() for key, cls in self.providers.items()}
        self.expire = expire
        self.cache = Cache(Path(gettempdir()) / "lunch_menu_cache")

    async def get_providers(self):
        return list(self.providers.keys())

    async def get_menu(self, provider: str):
        instance = self.instances[provider]
        result = self.cache.get(provider)

        if result is None:
            try:
                result = await instance.get_menu()
            except:
                logging.exception(provider)
                result = None
                
            if result is not None:
                self.cache.set(provider, result, expire = self.expire)

        return {
            "name": instance.name,
            "url": instance.url,
            "menu": result if result is not None else None
        }
