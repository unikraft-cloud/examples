FROM --platform=$BUILDPLATFORM python:3.12-bookworm AS build

WORKDIR /app

COPY requirements.txt /app

RUN apt update && \
    apt-get install -y --no-install-suggests --no-install-recommends libev-dev && \
    pip3 install -r requirements.txt --no-cache-dir

RUN set -xe; \
    /usr/sbin/ldconfig /usr/local/lib

FROM --platform=$BUILDPLATFORM build AS static
ADD . /app
RUN python3 manage.py collectstatic --noinput

FROM --platform=$BUILDPLATFORM build AS db
ADD . /app
RUN python3 manage.py migrate && \
    DJANGO_SUPERUSER_PASSWORD=unikraft python3 manage.py createsuperuser --noinput --username unikraft --email mail@example.com

FROM --platform=$BUILDPLATFORM scratch

COPY --from=build /usr/local/lib /usr/local/lib
COPY --from=build /usr/local/bin/python3 /usr/bin/python3
COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=build /usr/lib/x86_64-linux-gnu/libz.so.1 /usr/lib/x86_64-linux-gnu/libz.so.1
COPY --from=build /usr/lib/x86_64-linux-gnu/libcrypto.so.3 /usr/lib/x86_64-linux-gnu/libcrypto.so.3
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=build /etc/ld.so.cache /etc/ld.so.cache

COPY --from=build /usr/lib/x86_64-linux-gnu/libev.so.4 /usr/lib/x86_64-linux-gnu/libev.so.4
COPY --from=build /usr/lib/x86_64-linux-gnu/libsqlite3.so.0 /usr/lib/x86_64-linux-gnu/libsqlite3.so.0

ADD manage.py main.py /app/
ADD helloworld /app/helloworld/

COPY --from=static /app/static /app/static
COPY --from=db /app/db.sqlite3 /app/db.sqlite3
