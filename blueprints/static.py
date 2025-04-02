from sanic import Blueprint

blueprint = Blueprint("static")
blueprint.static("/", "templates/index.html", name = "html")
blueprint.static("/static", "static/", name = "static")