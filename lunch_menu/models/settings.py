from functools import cache
from typing import Annotated
from fastapi import Depends
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    establishments: list[str] = []
    establishments_module: str = "lunch_menu.establishments"
    highlighted_words: list[str] = []
    redis_url: str = "redis://localhost"
    cache_expiration: int = 600
    session_expiration: int = 604800
    timeout: int = 5
    user_agent: str | None = None
    oauth2_clients: dict[str, str] | None = None

@cache
def get_settings():
    return Settings()

SettingsDependency = Annotated[Settings, Depends(get_settings)]