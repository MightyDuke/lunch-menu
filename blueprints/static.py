from sanic import Blueprint

blueprint = Blueprint("static")

blueprint.static("/", "assets/index.html", name = "home")
blueprint.static("/static", "assets/static/", name = "static")