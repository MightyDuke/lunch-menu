from fastapi import APIRouter

router = APIRouter()
router.frontend("/", directory = f"web/src/", fallback = None)