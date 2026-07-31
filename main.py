from fastapi import FastAPI
from lunch_menu.routers import router as api_router
from web.router import router as web_router

app = FastAPI(
    title = "Lunch Menu"
)

app.include_router(api_router, prefix = "/api")
app.include_router(web_router)