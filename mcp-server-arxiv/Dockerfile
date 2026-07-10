FROM --platform=$BUILDPLATFORM python:3.11-slim AS build

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

FROM --platform=$BUILDPLATFORM python:3.11-slim

COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

COPY --from=ghcr.io/astral-sh/uv:0.9.14 /uv /uvx /bin/
RUN uv tool install arxiv-mcp-server

COPY ./server.py /src/server.py
