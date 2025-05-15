from sanic import Sanic
from blueprints import api_blueprint, static_blueprint
from services import LunchMenuService

app = Sanic("lunch_menu")
app.config.OAS = False

lunch_menu_service = LunchMenuService(expire = app.config.FETCH_EXPIRE)
app.ext.dependency(lunch_menu_service)

app.blueprint(static_blueprint)
app.blueprint(api_blueprint)
