FROM python:3.13

RUN apt update && \
    apt install -y locales-all && \
    pip install pipenv

WORKDIR /app
COPY . .
RUN pipenv install --system

ENTRYPOINT sanic app \
    --fast \
    --host 0.0.0.0 \
    --port 80