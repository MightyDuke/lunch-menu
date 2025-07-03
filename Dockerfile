FROM node:24.3 AS build
WORKDIR /app

COPY web/ .
RUN npm install && npx parcel build "index.html"

FROM python:3.13
WORKDIR /app
EXPOSE 80

RUN pip install --no-cache-dir pipenv

COPY . .
RUN rm -rf web
COPY --from=build /app/dist/ web/

RUN pipenv install --system

ENTRYPOINT [ \
    "sanic", "app", \
    "--fast", \
    "--no-access-logs", \
    "--host", "0.0.0.0", \
    "--port", "80" \
]
