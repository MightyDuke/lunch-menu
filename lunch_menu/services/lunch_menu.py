import importlib
import inspect
import pkgutil
from asyncio import CancelledError
from collections import OrderedDict
from logging import getLogger
from typing import Annotated
from aiocache import Cache
from httpx import AsyncClient
from fastapi import Depends, HTTPException
from lunch_menu.providers.base import Provider
from lunch_menu.settings import Settings, get_settings

logger = getLogger("uvicorn.error")

class LunchMenuService:
    @staticmethod
    def discover_establishments(base_module_path: str):
        result = {}

        for _, module_name, _ in pkgutil.iter_modules(importlib.import_module(base_module_path).__path__):
            full_module_name = f"{base_module_path}.{module_name}"

            module = importlib.import_module(full_module_name)

            for _, cls in inspect.getmembers(
                module,
                lambda member, module_name = full_module_name: inspect.isclass(member) and issubclass(member, Provider) and member.__module__ == module_name,
            ):
                result[module_name.replace("_", "-")] = cls

        return result

    def __init__(self, settings: Annotated[Settings, Depends(get_settings)]):
        self.highlighted_words = settings.highlighted_words

        self.client = AsyncClient(http2 = True, timeout = settings.timeout)
        self.cache = Cache.from_url(settings.cache_url)
        self.instances = OrderedDict()

        self.establishments = self.discover_establishments(settings.establishments_module)
        logger.info(f"Discovered {len(self.establishments.keys())} establishments: {str.join(", ", self.establishments.keys())}")

        for establishment in settings.establishments:
            if establishment not in self.establishments:
                logger.warning(f"Establishment not found: {establishment}")
                continue

            cls = self.establishments[establishment]

            self.instances[establishment] = cls(
                key = establishment, 
                client = self.client, 
                cache = self.cache, 
                expiration = settings.cache_expiration
            )

    def highlight_items(self, menu: dict):
        for day in menu.values():
            for item in day:
                item["highlight"] = any(word.lower() in item["name"].lower() for word in self.highlighted_words)

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
            raise HTTPException(404, f"Establishment \"{establishment}\" not found")

        try:
            result = await instance.get_menu()
            self.highlight_items(result)
        except NotImplementedError:
            raise HTTPException(400, f"Establishment \"{establishment}\" doesn't provide a menu")
        except CancelledError:
            result = {}
        except:
            logger.exception(f"{instance.__class__.__name__}, {establishment} - get_menu")
            result = {}
            raise

        return result