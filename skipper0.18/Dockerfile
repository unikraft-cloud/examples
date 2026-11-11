FROM --platform=$BUILDPLATFORM tonistiigi/xx:1.10.0 AS xx

FROM --platform=$BUILDPLATFORM golang:1.21.4-bookworm AS build

COPY --from=xx / /

WORKDIR /

RUN set -xe; \
    wget -O skipper.tar.gz "https://github.com/zalando/skipper/archive/refs/tags/v0.18.51.tar.gz"; \
    tar xzvf skipper.tar.gz;

WORKDIR /skipper-0.18.51

ARG TARGETPLATFORM

RUN set -xe; \
    CGO_ENABLED=0 xx-go build -o /usr/bin/skipper ./cmd/skipper; \
    xx-verify --static /usr/bin/skipper

FROM scratch

COPY --from=build /usr/bin/skipper /usr/bin/skipper
COPY ./rootfs/ /
