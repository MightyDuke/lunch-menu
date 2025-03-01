from datetime import date, timedelta
from sanic import Request, Blueprint
from sanic.response import json
from sanic_ext import render, cors
from lunch_menu.services import LunchMenuProvider

blueprint = Blueprint("lunch_menu")
blueprint.static("/static", "lunch_menu/static/", name = "static")

async def menu(lunch_menu_provider: LunchMenuProvider, selected_date: date):
    now = date.today()
    monday = now - timedelta(days = now.isoweekday() - 1)
    days_of_week = [monday + timedelta(days = i) for i in range(5)]

    return await render("index.html", context = {
        "providers": await lunch_menu_provider.get_all_menus(),
        "selected_date": selected_date,
        "days_of_week": days_of_week,
        "now": now
    })

@blueprint.get("/")
def index(request: Request, lunch_menu_provider: LunchMenuProvider):
    return menu(lunch_menu_provider, date.today())

@blueprint.get("/<selected_date:ymd>")
def index_date(request: Request, lunch_menu_provider: LunchMenuProvider, selected_date: date):
    return menu(lunch_menu_provider, selected_date)

@blueprint.get("/api/menu")
@cors(origin = "*")
async def api_menu(request: Request, lunch_menu_provider: LunchMenuProvider):
    result = await lunch_menu_provider.get_all_menus()
    return json(result)

