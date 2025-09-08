from sanic import Blueprint, HTTPResponse, NotFound, Request

blueprint = Blueprint("web")

@blueprint.on_request
async def on_request(request: Request):
    if request.path == "/index.html":
        raise NotFound("File not found")

@blueprint.on_response
async def on_response(request: Request, response: HTTPResponse):
    if response.content_type is None:
        return
    
    if "text/html" in response.content_type:
        response.headers["Cache-Control"] = "no-cache"
        response.headers["Content-Security-Policy"] = "default-src 'self' 'unsafe-eval' 'unsafe-inline'"
    elif response.status == 200: 
        response.headers["Cache-Control"] = "public, max-age=31536000, immutable"

blueprint.static("/", "web/app/", index = "index.html", name = "static")
