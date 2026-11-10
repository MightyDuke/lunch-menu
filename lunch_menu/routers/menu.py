from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from lunch_menu.models.establishments import EstablishmentEntriesResponse
from lunch_menu.models.menu import MenuForEstablishmentResponse
from lunch_menu.services.lunch_menu import LunchMenuService

router = APIRouter(tags = ["Menu"])

@router.get(
    "/establishments", 
    name = "Get Establishments", 
    description = 
        "Return all available establishments. Link only menu "
        "means that the given establishment doesn't provide a menu and "
        "no attempt should be made to get a menu.", 
    tags = ["MCP"],
    operation_id = "get_available_establishments"
)
async def establishments(
    lunch_menu: Annotated[LunchMenuService, Depends()]
) -> EstablishmentEntriesResponse:
    establishments = await lunch_menu.get_establishments()
    return EstablishmentEntriesResponse(establishments)

@router.get(
    "/establishments/{establishment}", 
    name = "Get Menu", 
    description = 
        "Get menu for the given establishment. If the user asks for a specific day, "
        "make sure to also include the weekly menu.",
    tags = ["MCP"],
    operation_id = "get_menu_for_establishment"
)
async def establishment(
    establishment: str, 
    lunch_menu: Annotated[LunchMenuService, Depends()]
) -> MenuForEstablishmentResponse:
    try:
        menu = await lunch_menu.get_menu(establishment)
    except ValueError as error:
        raise HTTPException(404, str(error))
    except NotImplementedError as error:
        raise HTTPException(400, str(error))
    except Exception as error:
        raise HTTPException(500, "An error has occured while obtaining the menu")

    return MenuForEstablishmentResponse(menu)