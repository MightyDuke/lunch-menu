from sanic import Config, Request, Sanic, text
from lunch_menu.blueprint import blueprint as lunch_menu_api_blueprint
from web.blueprint import blueprint as lunch_menu_web_blueprint

def list_converter(value: str) -> list[str]:
    value = value.strip()

    if not value.startswith("[") or not value.endswith("]"):
        raise ValueError()
    
    return [
        item.strip() 
        for item 
        in value.removeprefix("[").removesuffix("]").split(",")
    ]

app = Sanic("lunch_menu", config = Config(env_prefix = "LUNCH_MENU_", converters = [list_converter]))

app.blueprint(lunch_menu_api_blueprint, url_prefix = "/api")
app.blueprint(lunch_menu_web_blueprint)

@app.get("/robots.txt")
async def robots_txt(request: Request):
    return text("User-agent: *\nDisallow: /")
