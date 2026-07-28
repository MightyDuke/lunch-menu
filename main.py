from fastapi import FastAPI
from lunch_menu.router import router as lunch_menu_api_router
from web.router import router as lunch_menu_web_router

app = FastAPI(
    title = "Lunch Menu"
)

app.include_router(lunch_menu_api_router, prefix = "/api")
app.include_router(lunch_menu_web_router)