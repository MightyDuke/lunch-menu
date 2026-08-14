FROM node:24.3-alpine AS frontend
WORKDIR /app

COPY web/src/ .
RUN npm install && npx parcel build "index.html" "404.html" --dist-dir "dist/"

FROM python:3.14-alpine
WORKDIR /app
EXPOSE 8000

ENV UV_PROJECT_ENVIRONMENT=/usr/local

RUN pip install --no-cache-dir uv
COPY . .
RUN uv sync --locked

COPY --from=frontend /app/dist/ web/dist/

ENTRYPOINT [ "fastapi", "run" ]