from functools import cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    establishments: list[str] = []
    establishments_module: str = "lunch_menu.establishments"
    cache_url: str = "memory://"
    cache_expiration: int = 600
    timeout: int = 5
    highlighted_words: list[str] = []

@cache
def get_settings():
    return Settings()