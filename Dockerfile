FROM node:24.3-alpine AS frontend
WORKDIR /app

COPY web/src/ .
RUN npm install && npx parcel build "index.html"

FROM python:3.14-alpine
WORKDIR /app
EXPOSE 80

RUN pip install --no-cache-dir poetry
COPY . .
RUN poetry install

RUN rm -rf web/src/
COPY --from=frontend /app/dist/ web/src/

ENTRYPOINT [ "poetry", "run", "fastapi", "run" ]