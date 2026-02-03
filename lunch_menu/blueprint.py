from lunch_menu import examples
from sanic import HTTPResponse, Sanic, Request, Blueprint
from sanic.response import json
from sanic_ext import openapi, serializer
from sanic_ext.extensions.openapi.definitions import Response
from lunch_menu.services import LunchMenuService

blueprint = Blueprint("API")

@blueprint.before_server_start
async def before_server_start(app: Sanic):
    app.ext.dependency(LunchMenuService(app.config))

@blueprint.on_response
async def on_response(request: Request, response: HTTPResponse):
    if response.status == 200:
        response.headers["Cache-Control"] = "private, max-age=60, must-revalidate"

@blueprint.get("/establishments")
@openapi.definition(
    summary = "Get all establishments",
    description = "Get all available establishments. Only those with `linkOnly` set to true may provide a menu.",
    response = [
        Response(status = 200, description = "Successful response", content = {
            "application/json": {
                "schema": examples.establishment_list_schema,
                "example": examples.establishment_list_example
            }
        }) 
    ]
)
@serializer(json)
async def establishments(request: Request, lunch_menu_service: LunchMenuService):
    establishments = await lunch_menu_service.get_establishments()
    return establishments

@blueprint.get("/establishments/<establishment:str>")
@openapi.definition(
    summary = "Get an establishment menu",
    description = "Get a weekly menu of an establishment. The key of the returned object is either an ISO date or the word `week` if the items are available for the whole week.",
    response = [
        Response(status = 200, description = "Successful response", content = {
            "application/json": {
                "schema": examples.establishment_menu_schema,
                "example": examples.establishment_menu_example
            }
        }),
        Response(status = 400, description = "Establishment doesn't provide a menu", content = {
            "application/json": {
                "schema": examples.sanic_error_schema,
                "example": examples.establishment_doesnt_provide_menu_example
            }
        })
    ]
)
@serializer(json)
async def establishment(request: Request, establishment: str, lunch_menu_service: LunchMenuService):
    menu = await lunch_menu_service.get_menu(establishment)
    return menu
