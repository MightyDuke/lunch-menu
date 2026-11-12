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
        "Return all available establishments. "
        "The keys of the dictionary returned signify an establishment. It can be used as "
        "a parameter in the `get_menu_for_establishment` operation."
        "Link only menu means that the given establishment doesn't provide a menu and "
        "no attempt should be made to get a menu.",
    operation_id = "get_available_establishments"
)
async def establishments(lunch_menu: Annotated[LunchMenuService, Depends()]) -> EstablishmentEntriesResponse:
    establishments = await lunch_menu.get_establishments()
    return EstablishmentEntriesResponse(establishments)

@router.get(
    "/establishments/{establishment}", 
    name = "Get Menu", 
    description = 
        "Get the menu for the given establishment. Use the dictionary key acquired from "
        "`get_available_establishments` as a paramater. If the user asks for a specific day, "
        "make sure to also include the weekly menu. Weekly menu has `week` as the key.",
    operation_id = "get_menu_for_establishment",
    responses = {
        404: {
            "description": "Establishment doesn't exist",
            "model": str,
        },
        400: {
            "description": "Establishment doesn't provide a menu",
            "model": str,
        }
    }
)
async def establishment(establishment: str, lunch_menu: Annotated[LunchMenuService, Depends()]) -> MenuForEstablishmentResponse:
    try:
        menu = await lunch_menu.get_menu(establishment)
    except ValueError as error:
        raise HTTPException(404, str(error))
    except NotImplementedError as error:
        raise HTTPException(400, str(error))

    return MenuForEstablishmentResponse(menu)
