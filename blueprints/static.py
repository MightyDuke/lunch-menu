from sanic import Blueprint

blueprint = Blueprint("static")

blueprint.static("/", "templates/index.html", name = "home")
blueprint.static("/static", "static/", name = "static")