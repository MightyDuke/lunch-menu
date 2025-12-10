# Lunch Menu

An app for local restaurant lunch menus around the place I work at.

## Enviromental variables

- `LUNCH_MENU_CACHE_URL`: Cache url. Supports [aiocache](https://github.com/aio-libs/aiocache) urls, i.e. `memory://` or `redis://<redis_url>`. Redis is recommended.
- `LUNCH_MENU_CACHE_EXPIRATION`: How long should the cache time to live should be, in seconds.

## Run with Docker

The easiest way to run this app is with Docker, simply clone the repo and run `docker compose up -d`.
