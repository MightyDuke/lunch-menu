import asyncio
import logging
from lunch_menu.providers.toni import ToniProvider
from lunch_menu.providers.boasi import BoasiProvider
from lunch_menu.providers.paleta import PaletaProvider
from lunch_menu.providers.blesk import BleskProvider

class LunchMenuProvider:
    restaurants = [
        ToniProvider,
        BoasiProvider,
        PaletaProvider,
        BleskProvider, 
    ]

    def __init__(self):
        self.instances = [cls() for cls in self.restaurants]

    @staticmethod
    async def task_factory(instance):
        try:
            result = await instance.get_menu()
        except:
            logging.exception(instance.class_name)
            result = None
        
        return (instance, result)

    async def get_all_menus(self):
        result = await asyncio.gather(*(self.task_factory(instance) for instance in self.instances), return_exceptions = True)

        return [
            {
                "name": instance.name,
                "url": instance.url,
                "menu": result if not result is None else None
            }
            for instance, result
            in result
        ]