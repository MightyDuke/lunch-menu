from contextlib import asynccontextmanager
from logging import getLogger
from fastapi import APIRouter, FastAPI
from lunch_menu.models.settings import Settings
from lunch_menu.services.lunch_menu import LunchMenuService
from lunch_menu.services.redis_client import RedisClientService
from lunch_menu.services.session import SessionService
from .menu import router as menu_router
from .session import router as session_router
from .voting import router as voting_router

logger = getLogger("uvicorn.error")

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()

    establishments = LunchMenuService.discover_establishments(settings.establishments_module)
    logger.info(f"Discovered {len(establishments.keys())} establishments: {str.join(", ", establishments.keys())}")

    redis_pool = RedisClientService.create_connection_pool(settings.redis_url)

    issuers = await SessionService.discover_issuers([
        "https://accounts.google.com"
    ])
    logger.info(f"Discovered {len(issuers.keys())} OAuth2 issuers: {str.join(", ", (key for key in issuers.keys()))}")

    app.state.establishments = establishments
    app.state.redis_pool = redis_pool
    app.state.issuers = issuers

    yield 

    await app.state.redis_pool.aclose()

router = APIRouter(lifespan = lifespan)

router.include_router(menu_router)
router.include_router(session_router)
router.include_router(voting_router)