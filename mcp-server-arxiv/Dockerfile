# uv binary for the target architecture.
FROM --platform=linux/x86_64 ghcr.io/astral-sh/uv:0.9.14 AS uv

FROM --platform=linux/x86_64 python:3.11-slim AS build

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

FROM --platform=linux/x86_64 python:3.11-slim

COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

COPY --from=uv /uv /uvx /bin/
RUN uv tool install arxiv-mcp-server

COPY ./server.py /src/server.py
