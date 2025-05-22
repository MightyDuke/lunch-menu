from sanic import Request, Blueprint
from sanic.response import json
from sanic_ext import serializer
from sanic_ext import cors
from services import LunchMenuService

blueprint = Blueprint("api", url_prefix = "api")

@blueprint.get("/providers")
@serializer(json)
@cors(origin = "*")
async def providers(request: Request, lunch_menu_service: LunchMenuService):
    result = await lunch_menu_service.get_providers()
    return result

@blueprint.get("/providers/<provider:str>")
@serializer(json)
@cors(origin = "*")
async def provider(request: Request, lunch_menu_service: LunchMenuService, provider: str):
    menu = await lunch_menu_service.get_menu(provider)
    return menu