import asyncio
import logging
import pickle
from datetime import datetime, timedelta
from tempfile import gettempdir
from pathlib import Path
from lunch_menu.providers.toni import ToniProvider
from lunch_menu.providers.boasi import BoasiProvider
from lunch_menu.providers.paleta import PaletaProvider
from lunch_menu.providers.blesk import BleskProvider
from lunch_menu.providers.phobo import PhoboProvider
from lunch_menu.providers.hodonanka import HodonankaProvider

class LunchMenuProvider:
    restaurants = [
        ToniProvider,
        BoasiProvider,
        PaletaProvider,
        BleskProvider, 
        PhoboProvider,
        HodonankaProvider
    ]

    CACHE_PATH = Path(gettempdir()) / "lunch_menu_cache.bin"

    def __init__(self, expire: timedelta):
        self.instances = [cls() for cls in self.restaurants]
        self.expire = timedelta(seconds = expire)

    @staticmethod
    async def task_factory(instance):
        try:
            result = await instance.get_menu()
        except:
            logging.exception(instance.class_name)
            result = None
        
        return instance, result

    async def get_all_menus(self):
        try:
            with open(self.CACHE_PATH, "rb") as file:
                expire, menus = pickle.load(file)
        except:
            expire = None

        if expire is None or expire <= datetime.now():
            menus = await asyncio.gather(*(self.task_factory(instance) for instance in self.instances))

            with open(self.CACHE_PATH, "wb") as file:
                pickle.dump((datetime.now() + self.expire, menus), file)    
        
        return [
            {
                "name": instance.name,
                "url": instance.url,
                "menu": result if result is not None else None
            }
            for instance, result
            in menus
        ]
