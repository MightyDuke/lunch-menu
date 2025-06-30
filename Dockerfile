FROM node:24.3 AS builder

WORKDIR /app

COPY . .
RUN npm install --prefix "web/"

FROM python:3.13

WORKDIR /app

RUN pip install pipenv
COPY --from=builder /app .
RUN pipenv install --system

ENTRYPOINT [ \
    "sanic", "app", \
    "--fast", \
    "--no-access-logs", \
    "--host", "0.0.0.0", \
    "--port", "80" \
]
