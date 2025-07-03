from sanic import Blueprint

blueprint = Blueprint("web")
blueprint.static("/", "web/", index = "index.html", name = "static")