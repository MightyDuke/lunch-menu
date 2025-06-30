from sanic import Sanic
from blueprints.api import blueprint as api_blueprint
from blueprints.web import blueprint as static_blueprint
from services.lunch_menu import LunchMenuService

app = Sanic("lunch_menu")
app.config.OAS = False

lunch_menu_service = LunchMenuService(expire = app.config.get("FETCH_EXPIRE", 600))
app.ext.dependency(lunch_menu_service)

app.blueprint(static_blueprint)
app.blueprint(api_blueprint)
