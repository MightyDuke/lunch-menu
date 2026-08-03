FROM node:24.3 AS frontend
WORKDIR /app

COPY web/app/ .
RUN npm install && npx parcel build "index.html"

FROM python:3.14
WORKDIR /app
EXPOSE 80

RUN pip install --no-cache-dir poetry
COPY . .
RUN poetry install

RUN rm -rf web/app/
COPY --from=frontend /app/dist/ web/app/

ENTRYPOINT [ "poetry", "run", "fastapi", "run", "--workers", "2" ]