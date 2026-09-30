FROM python:3.11-slim AS build

WORKDIR /app

RUN set -xe; \
    /usr/sbin/ldconfig /usr/local/lib

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


FROM gcr.io/distroless/python3-debian12

COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/dist-packages

COPY ./server.py /src/server.py
