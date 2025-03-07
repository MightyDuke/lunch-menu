from sanic import Request, Blueprint
from sanic.exceptions import NotFound, SanicException
from sanic.response import json
from sanic_ext import cors
from lunch_menu.services import LunchMenuService

blueprint = Blueprint("api", url_prefix = "api")

@blueprint.exception(Exception)
async def exceptions(request: Request, exception: Exception):
    status = exception.status_code if isinstance(exception, SanicException) else 500

    return json({
        "error": True,
        "status": exception.status_code
    }, status = status)

@blueprint.get("/providers")
@cors(origin = "*")
async def providers(request: Request, lunch_menu_provider: LunchMenuService):
    result = await lunch_menu_provider.get_providers()
    return json(result)

@blueprint.get("/providers/<provider:str>")
@cors(origin = "*")
async def provider(request: Request, lunch_menu_provider: LunchMenuService, provider: str):
    try:
        menu = await lunch_menu_provider.get_menu(provider)
    except KeyError:
        raise NotFound()
    
    return json(menu)