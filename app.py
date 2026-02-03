from converters import list_converter
from sanic import Config, Sanic
from sanic_ext import openapi
from lunch_menu.blueprint import blueprint as lunch_menu_api_blueprint
from web.blueprint import blueprint as lunch_menu_web_blueprint

config = Config(env_prefix = "LUNCH_MENU_", converters = [list_converter])

app = Sanic("lunch_menu", config = config)
app.ext.openapi.describe("Lunch Menu", version = "1.0.0")

app.blueprint(lunch_menu_api_blueprint, url_prefix = "/api")
app.blueprint(lunch_menu_web_blueprint)

openapi.exclude(bp = lunch_menu_web_blueprint)