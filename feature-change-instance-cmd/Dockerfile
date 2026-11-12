FROM gcc:13.2.0-bookworm AS build

WORKDIR /src

COPY ./http_server.c /src/http_server.c
COPY ./http_server_args.c /src/http_server_args.c

RUN set -xe; \
    gcc -Wall -Wextra -static -o /http_server http_server.c; \
    gcc -Wall -Wextra -static -o /http_server_args http_server_args.c; \
    file /http_server | grep -q "statically linked"; \
    file /http_server_args | grep -q "statically linked"

FROM scratch

COPY --from=build /http_server /http_server
COPY --from=build /http_server_args /http_server_args
