from logging import getLogger
from fastapi_singleton import singleton

logger = getLogger("uvicorn.error")

@singleton
class LoggerService:
    def __init__(self):
        pass

    def info(self, text: str):
        logger.info(text)