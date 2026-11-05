FROM python:3.12-bookworm AS build

RUN set -xe; \
    /usr/sbin/ldconfig /usr/local/lib

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r requirements.txt --no-cache-dir


FROM gcr.io/distroless/cc-debian12:latest

COPY --from=build /usr/local/lib /usr/local/lib
COPY --from=build /usr/local/bin/python3 /usr/bin/python3
COPY --from=build /usr/local/lib/libpython3.12.so.1.0 /usr/lib/x86_64-linux-gnu/libpython3.12.so.1.0
COPY --from=build /usr/lib/x86_64-linux-gnu/libz.so.1 /usr/lib/x86_64-linux-gnu/libz.so.1

COPY ./server.py /src/server.py
