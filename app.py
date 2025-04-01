from sanic import Sanic
from blueprints import api_blueprint, static_blueprint
from services import LunchMenuService

app = Sanic("lunch_menu")

lunch_menu_service = LunchMenuService(app.config.get("FETCH_EXPIRE", 600))

app.ext.dependency(lunch_menu_service)
app.blueprint(static_blueprint)
app.blueprint(api_blueprint)
