FROM gcc:13.2.0-bookworm AS build

WORKDIR /src

COPY ./http_server.cpp /src/http_server.cpp

RUN set -xe; \
    g++ -Wall -Wextra -static -o /http_server http_server.cpp; \
    file /http_server | grep -q "statically linked"

FROM scratch

COPY --from=build /http_server /http_server
