FROM node:24.3 AS frontend
WORKDIR /app

COPY web/app/ .
RUN npm install && npx parcel build "index.html"

FROM python:3.14
WORKDIR /app
EXPOSE 80

RUN pip install --no-cache-dir pipenv
COPY . .
RUN pipenv install --system

RUN rm -rf web/app/
COPY --from=frontend /app/dist/ web/app/

ENTRYPOINT [ \
    "sanic", "app", \
    "--fast", \
    "--no-access-logs", \
    "--host", "0.0.0.0", \
    "--port", "80" \
]
