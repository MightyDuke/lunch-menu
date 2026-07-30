from fastapi import APIRouter
import os.path

router = APIRouter()
router.frontend("/", directory = f"{os.path.dirname(__file__)}/src", fallback = None)