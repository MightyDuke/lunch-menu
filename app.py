from sanic import Sanic
from cashews import cache
from blueprints.api import blueprint as api_blueprint
from blueprints.web import blueprint as static_blueprint
from services.lunch_menu import LunchMenuService

app = Sanic("lunch_menu")
app.config.OAS = False

cache.setup(app.config.get("CACHE_URL", "disk://?directory=/tmp/lunch_menu"))

lunch_menu_service = LunchMenuService()
app.ext.dependency(lunch_menu_service)

app.blueprint(static_blueprint)
app.blueprint(api_blueprint)
