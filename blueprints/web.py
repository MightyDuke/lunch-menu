from sanic import Blueprint

blueprint = Blueprint("web")

blueprint.static("/", "web/index.html", name = "home")
blueprint.static("/static", "web/static/", name = "static")