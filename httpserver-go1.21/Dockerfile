FROM --platform=$BUILDPLATFORM tonistiigi/xx:1.10.0 AS xx

FROM --platform=$BUILDPLATFORM golang:1.21.3-bookworm AS build

COPY --from=xx / /

ARG TARGETPLATFORM

WORKDIR /src

COPY ./server.go /src/server.go

RUN set -xe; \
    CGO_ENABLED=0 xx-go build -tags netgo -o /server server.go; \
    xx-verify --static /server

FROM scratch

COPY --from=build /server /server
