FROM python:3.13-slim

WORKDIR /app
RUN apt update && \
    apt install -y locales-all && \
    pip install pipenv

COPY . .
RUN pipenv install --system

ENV LC_TIME="cs_CZ"

ENTRYPOINT [ \
    "sanic", "lunch_menu.app", \
    "--fast", \
    "--host", "0.0.0.0", \
    "--port", "80" \
]