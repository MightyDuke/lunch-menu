from sanic import Blueprint

blueprint = Blueprint("static")
blueprint.static("/", "lunch_menu/templates/index.html", name = "html")
blueprint.static("/static", "lunch_menu/static/", name = "static")