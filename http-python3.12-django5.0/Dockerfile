FROM python:3.12-bookworm AS base

WORKDIR /app

COPY requirements.txt /app

RUN apt update && \
    apt-get install -y --no-install-suggests --no-install-recommends libev-dev && \
    pip3 install -r requirements.txt --no-cache-dir

FROM base AS static
ADD . /app
RUN python3 manage.py collectstatic --noinput

FROM scratch

COPY --from=base /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=base /usr/lib/x86_64-linux-gnu/libev.so.4 /usr/lib/x86_64-linux-gnu/libev.so.4
COPY --from=base /usr/lib/x86_64-linux-gnu/libsqlite3.so.0 /usr/lib/x86_64-linux-gnu/libsqlite3.so.0
ADD manage.py main.py /app/
ADD helloworld /app/helloworld/
COPY --from=static /app/static /app/static
