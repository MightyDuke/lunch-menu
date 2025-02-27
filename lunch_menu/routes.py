from datetime import date, timedelta
from sanic import Request, Blueprint
from sanic.response import json
from sanic_ext import render, cors
from lunch_menu.services import LunchMenuProvider

blueprint = Blueprint("lunch_menu")
blueprint.static("/static", "lunch_menu/static/", name = "static")

def days_of_week():
    now = date.today()
    monday = now - timedelta(days = now.isoweekday() - 1)
    result = []

    for i in range(5):
        d = monday + timedelta(days = i)
        result.append((d.strftime("%A").title(), d))

    return result

@blueprint.get("/")
async def index(request: Request, lunch_menu_provider: LunchMenuProvider):
    result = await lunch_menu_provider.get_all_menus()
    selected_date = date.today()

    return await render("index.html", context = {
        "providers": result,
        "selected_date": selected_date,
        "days_of_week": days_of_week()
    })

@blueprint.get("/date/<selected_date:ymd>")
async def index_date(request: Request, lunch_menu_provider: LunchMenuProvider, selected_date: date):
    result = await lunch_menu_provider.get_all_menus()

    return await render("index.html", context = {
        "providers": result,
        "selected_date": selected_date,
        "days_of_week": days_of_week()
    })

@blueprint.get("/api/menu")
@cors(origin = "*")
async def api_menu(request: Request, lunch_menu_provider: LunchMenuProvider):
    result = await lunch_menu_provider.get_all_menus()
    return json(result)

