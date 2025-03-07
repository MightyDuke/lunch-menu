from sanic import Sanic
from lunch_menu.blueprints import api_blueprint, static_blueprint
from lunch_menu.services import LunchMenuService

app = Sanic("lunch_menu")

app.ext.dependency(LunchMenuService(app.config.get("FETCH_EXPIRE", 600)))
app.blueprint(static_blueprint)
app.blueprint(api_blueprint)

