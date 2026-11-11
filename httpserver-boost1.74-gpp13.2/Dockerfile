FROM gcc:13.2.0-bookworm AS build

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends libboost-system1.74-dev libboost-thread1.74-dev; \
    rm -rf /var/lib/apt/lists/*

WORKDIR /src

COPY ./http_server.cpp /src/http_server.cpp

RUN set -xe; \
    g++ -Wall -Wextra -static -o /http_server http_server.cpp -lboost_system -lboost_thread -lpthread; \
    file /http_server | grep -q "statically linked"

FROM scratch

COPY --from=build /http_server /http_server
