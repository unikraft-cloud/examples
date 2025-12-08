FROM --platform=linux/x86_64 golang:1.21.3-bookworm AS build

WORKDIR /src

COPY ./server.go /src/server.go

RUN set -xe; \
    go build \
      -buildmode=pie \
      -ldflags "-linkmode external -extldflags -static-pie" \
      -tags netgo \
      -o /server server.go \
    ;

FROM scratch

COPY --from=build /server /server
