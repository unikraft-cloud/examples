FROM gcc:13.2.0-bookworm AS build

WORKDIR /src

COPY ./http_server.c /src/http_server.c

RUN set -xe; \
    gcc -Wall -Wextra -static -o /http_server http_server.c; \
    file /http_server | grep -q "statically linked"

FROM scratch

COPY --from=build /http_server /http_server
