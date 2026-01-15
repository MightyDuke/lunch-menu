from sanic import Blueprint, HTTPResponse, NotFound, Request

blueprint = Blueprint("web")

@blueprint.on_request
async def on_request(request: Request):
    if request.path.lower().endswith("/index.html"):
        raise NotFound("File not found")

@blueprint.on_response
async def on_response(request: Request, response: HTTPResponse):
    if response.content_type is None:
        return
    
    if "text/html" in response.content_type:
        response.headers["Cache-Control"] = "no-cache"
    elif response.status == 200: 
        response.headers["Cache-Control"] = "public, max-age=31536000, immutable"

blueprint.static("/", "web/app/index.html", name = "index")
blueprint.static("/static", "web/app/", name = "static")
