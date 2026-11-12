from functools import cache
from fastapi_singleton import singleton
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    establishments: list[str] = []
    establishments_module: str = "lunch_menu.establishments"
    redis_url: str = "redis://localhost"
    cache_expiration: int = 600
    session_expiration: int = 604800
    http_timeout: int = 5
    user_agent: str | None = None
    oauth2_clients: dict[str, str] = {}

@singleton
@cache
def get_settings():
    return Settings()