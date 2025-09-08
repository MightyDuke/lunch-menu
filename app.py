from sanic import Sanic
from lunch_menu.blueprint import blueprint as lunch_menu_api_blueprint
from web.blueprint import blueprint as lunch_menu_web_blueprint

app = Sanic("lunch_menu")

app.blueprint(lunch_menu_api_blueprint, url_prefix = "/api")
app.blueprint(lunch_menu_web_blueprint)
