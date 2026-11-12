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
    name = "Kam na oběd MCP",
    description = "1.2.1",
    include_operations = [
        "get_available_establishments",
        "get_menu_for_establishment",
        "get_votes_for_given_date"
    ],
    describe_all_responses = True
)

mcp.mount_http(mount_path = "/mcp")