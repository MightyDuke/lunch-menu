from sanic import HTTPResponse, Sanic, Request, Blueprint
from sanic.response import json
from sanic_ext import serializer
from lunch_menu.services import LunchMenuService

blueprint = Blueprint("API")

@blueprint.before_server_start
async def before_server_start(app: Sanic):
    app.ext.dependency(LunchMenuService(app.config))

@blueprint.on_response
async def on_response(request: Request, response: HTTPResponse):
    if response.status == 200:
        response.headers["Cache-Control"] = "private, must-revalidate"

@blueprint.get("/establishments")
@serializer(json)
async def establishments(request: Request, lunch_menu_service: LunchMenuService):
    establishments = await lunch_menu_service.get_establishments()
    return establishments

@blueprint.get("/establishments/<establishment:str>")
@serializer(json)
async def establishment(request: Request, establishment: str, lunch_menu_service: LunchMenuService):
    menu = await lunch_menu_service.get_menu(establishment)
    return menu
