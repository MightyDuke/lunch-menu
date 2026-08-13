FROM node:24.3-alpine AS frontend
WORKDIR /app

COPY web/src/ .
RUN npm install && npx parcel build "index.html" "404.html" --dist-dir "dist/"

FROM python:3.14-alpine
WORKDIR /app
EXPOSE 8000

RUN pip install --no-cache-dir poetry
COPY . .
RUN poetry config virtualenvs.create false && poetry install

COPY --from=frontend /app/dist/ web/dist/

ENTRYPOINT [ "fastapi", "run" ]