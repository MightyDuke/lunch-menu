from typing import Annotated
from fastapi import APIRouter, Depends
from .settings import get_settings
from .services.lunch_menu import LunchMenuService

router = APIRouter(
    dependencies = [
        Depends(get_settings),
        Depends(LunchMenuService)
    ]
)

@router.get("/establishments")
async def establishments(
    lunch_menu_service: Annotated[LunchMenuService, Depends()]
):
    return await lunch_menu_service.get_establishments()

@router.get("/establishments/{establishment}")
async def estabsliment( 
    establishment: str,
    lunch_menu_service: Annotated[LunchMenuService, Depends()]
):
    return await lunch_menu_service.get_menu(establishment)