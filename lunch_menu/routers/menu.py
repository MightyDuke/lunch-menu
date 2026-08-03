from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response
from lunch_menu.models.establishments import EstablishmentEntriesResponse
from lunch_menu.models.menu import HighlightedWordsResponse, MenuForEstablishmentResponse
from lunch_menu.services.lunch_menu import LunchMenuService

def add_private_cache_header(response: Response):
    response.headers["Cache-control"] = "private, must-revalidate"

router = APIRouter(tags=["Menu"])

@router.get(
    "/establishments",
    dependencies = [Depends(add_private_cache_header)],
    name = "Get Establishments",
    description = "Return all available establishments."
)
async def establishments(lunch_menu: Annotated[LunchMenuService, Depends()]) -> EstablishmentEntriesResponse:
    establishments = await lunch_menu.get_establishments()

    return EstablishmentEntriesResponse(establishments)

@router.get(
    "/establishments/{establishment}",
    dependencies = [Depends(add_private_cache_header)],
    name = "Get Menu",
    description = "Get menu for the given establishment."
)
async def establishment(establishment: str, lunch_menu: Annotated[LunchMenuService, Depends()]) -> MenuForEstablishmentResponse:
    try:
        menu = await lunch_menu.get_menu(establishment)
    except ValueError as error:
        raise HTTPException(404, str(error))
    except NotImplementedError as error:
        raise HTTPException(400, str(error))
    except Exception as error:
        # logger.exception(f"{establishment} - get_menu")
        raise HTTPException(500, "An error has occured while obtaining the menu")

    return MenuForEstablishmentResponse(menu)

@router.get(
    "/highlighted-words",
    dependencies = [Depends(add_private_cache_header)],
    name = "Get Highlighted Words",
    description = "Get words that highlight a menu item."
)
async def highlighted_words(lunch_menu: Annotated[LunchMenuService, Depends()]) -> HighlightedWordsResponse:
    words = lunch_menu.highlighted_words

    return HighlightedWordsResponse(words)

