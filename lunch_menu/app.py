import locale
from sanic import Sanic
from lunch_menu.routes import blueprint
from lunch_menu.services import LunchMenuProvider

locale.setlocale(locale.LC_TIME, "cs_CZ")

app = Sanic("lunch_menu")
app.config.OAS = False
app.config.TEMPLATING_PATH_TO_TEMPLATES = [
    "lunch_menu/templates/"
]

app.ext.dependency(LunchMenuProvider())
app.blueprint(blueprint)