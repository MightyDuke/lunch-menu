import importlib
import inspect
import pkgutil
from asyncio import CancelledError
from typing import Annotated
from fastapi import Depends
from fastapi_singleton import singleton
from lunch_menu.providers.base import Provider
from lunch_menu.models.settings import Settings, get_settings
from lunch_menu.services.http_client import HttpClientService
from lunch_menu.services.logger import LoggerService
from lunch_menu.services.redis_client import RedisClientService

def discover_establishments(module_path: str) -> dict[str, type]:
    result = {}

    for _, module_name, _ in pkgutil.iter_modules(importlib.import_module(module_path).__path__):
        full_module_name = f"{module_path}.{module_name}"
        module = importlib.import_module(full_module_name)

        for _, cls in inspect.getmembers(
            module,
            lambda member, module_name = full_module_name: inspect.isclass(member) and issubclass(member, Provider) and member.__module__ == module_name,
        ):
            result[module_name.replace("_", "-").lower()] = cls

    return result

@singleton
class LunchMenuService:
    def __init__(self, 
        settings: Annotated[Settings, Depends(get_settings)],
        http_client: Annotated[HttpClientService, Depends(HttpClientService)],
        redis_client: Annotated[RedisClientService, Depends(RedisClientService)],
        logger: Annotated[LoggerService, Depends(LoggerService)]
    ):
        self.establishment_classes = discover_establishments(settings.establishments_module)
        self.http_client = http_client 
        self.redis_client = redis_client

        self.enabled_establishments = settings.establishments
        self.expiration = settings.cache_expiration

        self.establishments = {
            establishment: cls(
                key = establishment,
                http_client = self.http_client,
                redis_client = self.redis_client,
                expiration = self.expiration,                
            )
            for establishment, cls
            in self.establishment_classes.items()
        }

        logger.info(f"Discovered {len(self.establishments)} establishments: {str.join(", ", self.establishments.keys())}")

    async def get_establishments(self) -> dict:
        result = {}

        for establishment_name in self.enabled_establishments:
            if establishment_name not in self.establishment_classes:
                continue

            establishment_class = self.establishment_classes[establishment_name]

            result[establishment_name] = {
                "name": establishment_class.name,
                "homepage": establishment_class.homepage,
                "linkOnly": establishment_class.link_only
            }

        return result

    async def get_menu(self, establishment: str) -> dict:
        instance = self.establishments.get(establishment, None)

        if instance is None:
            raise ValueError(f"Establishment {establishment} not found")

        try:
            result = await instance.get_menu()
        except CancelledError:
            result = {}

        return result