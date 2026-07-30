from contextlib import asynccontextmanager
from logging import getLogger
from typing import Annotated
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from lunch_menu.decorators import add_private_cache_header
from lunch_menu.models.establishments import EstablishmentEntriesModel
from lunch_menu.models.settings import Settings
from lunch_menu.services.lunch_menu import LunchMenuService
from lunch_menu.services.redis_client import RedisClientService
from lunch_menu.models.menu import HighlightedWordsModel, MenuForEstablishmentModel

logger = getLogger("uvicorn.error")

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()

    establishments = LunchMenuService.discover_establishments(settings.establishments_module)
    logger.info(f"Discovered {len(establishments.keys())} establishments: {str.join(", ", establishments.keys())}")

    redis_pool = RedisClientService.create_connection_pool(settings.redis_url)

    app.state.establishments = establishments
    app.state.redis_pool = redis_pool

    yield 

    await app.state.redis_pool.aclose()

router = APIRouter(lifespan = lifespan)

@router.get(
    "/establishments",
    dependencies = [Depends(add_private_cache_header)],
    name = "Get Establishments",
    description = "Return all available establishments."
)
async def establishments(lunch_menu: Annotated[LunchMenuService, Depends()]) -> EstablishmentEntriesModel:
    establishments = await lunch_menu.get_establishments()

    return EstablishmentEntriesModel(establishments)

@router.get(
    "/establishments/{establishment}",
    dependencies = [Depends(add_private_cache_header)],
    name = "Get Menu",
    description = "Get menu for the given establishment."
)
async def establishment(establishment: str, lunch_menu: Annotated[LunchMenuService, Depends()]) -> MenuForEstablishmentModel:
    try:
        menu = await lunch_menu.get_menu(establishment)
    except ValueError as error:
        raise HTTPException(404, str(error))
    except NotImplementedError as error:
        raise HTTPException(400, str(error))
    except error:
        logger.exception(f"{establishment} - get_menu")
        raise HTTPException(500, "An error has occured while obtaining the menu")

    return MenuForEstablishmentModel(menu)

@router.get(
    "/highlighted-words",
    dependencies = [Depends(add_private_cache_header)],
    name = "Get Highlighted Words",
    description = "Get words that are highlighted in the menu.`"
)
async def highlighted_words(lunch_menu: Annotated[LunchMenuService, Depends()]) -> HighlightedWordsModel:
    words = lunch_menu.highlighted_words

    return HighlightedWordsModel(words)