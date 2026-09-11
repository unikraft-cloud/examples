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

FROM --platform=linux/x86_64 gcr.io/distroless/static-debian13

COPY --from=build /server /server
