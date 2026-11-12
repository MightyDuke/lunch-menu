from fastapi import APIRouter
from fastapi_singleton import lifespan as singleton_lifespan
from .menu import router as menu_router
from .user import router as user_router
from .voting import router as voting_router

router = APIRouter(lifespan = singleton_lifespan)

router.include_router(menu_router)
router.include_router(user_router)
router.include_router(voting_router)
