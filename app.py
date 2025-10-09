from sanic import Request, Sanic, text
from lunch_menu.blueprint import blueprint as lunch_menu_api_blueprint
from web.blueprint import blueprint as lunch_menu_web_blueprint

app = Sanic("lunch_menu", env_prefix = "LUNCH_MENU_")

app.blueprint(lunch_menu_api_blueprint, url_prefix = "/api")
app.blueprint(lunch_menu_web_blueprint)

@app.get("/robots.txt")
async def robots_txt(request: Request):
    return text("User-agent: *\nDisallow: /")