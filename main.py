from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from lunch_menu.routers import router as api_router
from web.router import router as web_router

app = FastAPI(
    title = "Lunch Menu"
)

app.include_router(api_router, prefix = "/api")
app.include_router(web_router)

mcp = FastApiMCP(
    app,
    name = "Lunch Menu MCP",
    description = "1.2.0",
    include_tags = [
        "MCP"
    ]
)
mcp.mount_http(mount_path = "/mcp")