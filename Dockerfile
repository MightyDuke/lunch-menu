FROM python:3.13-slim

WORKDIR /app
RUN apt update && \
    pip install pipenv

COPY . .
RUN pipenv install --system

ENTRYPOINT [ \
    "sanic", "lunch_menu.app", \
    "--fast", \
    "--host", "0.0.0.0", \
    "--port", "80" \
]