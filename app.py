from sanic import Sanic
from lunch_menu.blueprint import blueprint as lunch_menu_api_blueprint

app = Sanic("lunch_menu")

app.blueprint(lunch_menu_api_blueprint, url_prefix = "/api")
app.static("/", "web/", index = "index.html", name = "static")