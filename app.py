from sanic import Config, Sanic
from converters import list_converter
from lunch_menu.blueprint import blueprint as lunch_menu_api_blueprint
from web.blueprint import blueprint as lunch_menu_web_blueprint

config = Config(env_prefix = "LUNCH_MENU_", converters = [list_converter])
config.OAS = False

app = Sanic("lunch_menu", config = config)

app.blueprint(lunch_menu_api_blueprint, url_prefix = "/api")
app.blueprint(lunch_menu_web_blueprint)