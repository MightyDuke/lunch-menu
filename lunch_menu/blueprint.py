from sanic import HTTPResponse, Sanic, Request, Blueprint
from sanic.response import json
from lunch_menu.services import LunchMenuService

blueprint = Blueprint("lunch_menu_api")

@blueprint.before_server_start
async def before_server_start(app: Sanic):
    cache_url = app.config.get("CACHE_URL", "memory://")
    expiration = app.config.get("CACHE_EXPIRATION", "600")

    app.ctx.lunch_menu_service = LunchMenuService(cache_url = cache_url, expiration = expiration)

@blueprint.on_response
async def on_response(request: Request, response: HTTPResponse):
    response.headers["Cache-Control"] = "no-store"

@blueprint.get("/establishments")
async def establishments(request: Request):
    lunch_menu_service = request.app.ctx.lunch_menu_service
    establishments = await lunch_menu_service.get_establishments()

    return json(establishments)

@blueprint.get("/establishments/<establishment:str>")
async def establishment(request: Request, establishment: str):
    lunch_menu_service = request.app.ctx.lunch_menu_service
    menu = await lunch_menu_service.get_menu(establishment)

    return json(menu)