import importlib
import inspect
import pkgutil
from asyncio import CancelledError
from typing import Annotated
from fastapi import Depends, Request
from lunch_menu.providers.base import Provider
from lunch_menu.models.settings import Settings, get_settings
from lunch_menu.services.http_client import HttpClientService
from lunch_menu.services.redis_client import RedisClientService

class LunchMenuService:
    @staticmethod
    def discover_establishments(module_path: str):
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

    def __init__(self, 
        request: Request,
        settings: Annotated[Settings, Depends(get_settings)],
        http_client: Annotated[HttpClientService, Depends()],
        redis_client: Annotated[RedisClientService, Depends()]
    ):
        self.establishment_classes = request.app.state.establishments

        self.http_client = http_client
        self.redis_client = redis_client

        self.highlighted_words = settings.highlighted_words
        self.enabled_establishments = settings.establishments
        self.expiration = settings.cache_expiration

    def _get_establishment_instance(self, establishment: str):
        if establishment not in self.establishment_classes:
            return

        cls = self.establishment_classes.get(establishment, None)

        if cls is None:
            return

        return cls(
            key = establishment, 
            http_client = self.http_client,
            redis_client = self.redis_client,
            expiration = self.expiration,
            highlighted_words = self.highlighted_words
        )        

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
        instance = self._get_establishment_instance(establishment)

        if instance is None:
            raise ValueError(f"Establishment {establishment} not found")

        try:
            result = await instance.get_menu()
        except CancelledError:
            result = {}

        return result