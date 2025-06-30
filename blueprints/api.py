import asyncio
from sanic import Request, Blueprint
from sanic.response import json
from sanic_ext import serializer, cors
from services.lunch_menu import LunchMenuService

blueprint = Blueprint("api", url_prefix = "api")

@blueprint.get("/providers")
@serializer(json)
@cors(origin = "*")
async def providers(request: Request, lunch_menu_service: LunchMenuService):
    return await lunch_menu_service.get_providers()

@blueprint.get("/providers/<provider:str>")
@serializer(json)
@cors(origin = "*")
async def provider(request: Request, lunch_menu_service: LunchMenuService, provider: str):
    return await lunch_menu_service.get_menu(provider)