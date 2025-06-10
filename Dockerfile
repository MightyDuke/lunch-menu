FROM python:3.13-slim

WORKDIR /app
RUN pip install pipenv

COPY . .
RUN pipenv install --system

ENV SANIC_PROXIES_COUNT=1

ENTRYPOINT [ \
    "sanic", "app", \
    "--fast", \
    "--no-access-logs", \
    "--host", "0.0.0.0", \
    "--port", "80" \
]