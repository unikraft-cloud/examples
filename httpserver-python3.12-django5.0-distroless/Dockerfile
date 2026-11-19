FROM python:3.12-bookworm AS build

WORKDIR /app

COPY requirements.txt /app

RUN apt update && \
    apt-get install -y --no-install-suggests --no-install-recommends libev-dev && \
    pip3 install -r requirements.txt --no-cache-dir

RUN set -xe; \
    /usr/sbin/ldconfig /usr/local/lib


FROM build AS static

ADD . /app

RUN python3 manage.py collectstatic --noinput


FROM build AS db

ADD . /app

RUN python3 manage.py migrate && \
    DJANGO_SUPERUSER_PASSWORD=unikraft python3 manage.py createsuperuser --noinput --username unikraft --email mail@example.com


FROM gcr.io/distroless/cc-debian12:latest

WORKDIR /app

COPY --from=build /usr/local/lib /usr/local/lib
COPY --from=build /usr/local/bin/python3 /usr/bin/python3
COPY --from=build /usr/local/lib/libpython3.12.so.1.0 /usr/lib/x86_64-linux-gnu/libpython3.12.so.1.0
COPY --from=build /usr/lib/x86_64-linux-gnu/libev.so.4 /usr/lib/x86_64-linux-gnu/libev.so.4
COPY --from=build /usr/lib/x86_64-linux-gnu/libsqlite3.so.0 /usr/lib/x86_64-linux-gnu/libsqlite3.so.0
COPY --from=build /usr/lib/x86_64-linux-gnu/libz.so.1 /usr/lib/x86_64-linux-gnu/libz.so.1

COPY manage.py main.py /app/
COPY helloworld /app/helloworld/

COPY --from=static /app/static /app/static
COPY --from=db /app/db.sqlite3 /app/db.sqlite3
