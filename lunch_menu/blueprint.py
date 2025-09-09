from sanic import HTTPResponse, Sanic, Request, Blueprint
from sanic.response import json
from lunch_menu.service import LunchMenuService

blueprint = Blueprint("lunch_menu_api")

@blueprint.before_server_start
async def before_server_start(app: Sanic):
    cache_url = app.config.get("CACHE_URL", "disk://?directory=/tmp/lunch_menu&shards=0")
    expiration = app.config.get("CACHE_EXPIRATION", "10m")

    app.ctx.lunch_menu_service = LunchMenuService(cache_url = cache_url, expiration = expiration)

@blueprint.on_response
async def on_response(request: Request, response: HTTPResponse):
    response.headers["Cache-Control"] = "no-store"

@blueprint.get("/providers")
async def providers(request: Request):
    lunch_menu_service = request.app.ctx.lunch_menu_service
    providers = await lunch_menu_service.get_providers()

    return json(providers)

@blueprint.get("/providers/<provider:str>")
async def provider(request: Request, provider: str):
    lunch_menu_service = request.app.ctx.lunch_menu_service
    menu = await lunch_menu_service.get_menu(provider)

    return json(menu)