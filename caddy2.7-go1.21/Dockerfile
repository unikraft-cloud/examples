FROM --platform=$BUILDPLATFORM tonistiigi/xx:1.10.0 AS xx

FROM --platform=$BUILDPLATFORM golang:1.21.3-bookworm AS build

COPY --from=xx / /

ARG TARGETPLATFORM

ARG CADDY_VERSION=2.7.6

WORKDIR /caddy

RUN --mount=type=cache,target=/root/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
      git; \
    git clone --depth=1 --branch v${CADDY_VERSION} https://github.com/caddyserver/caddy.git /caddy; \
    CGO_ENABLED=0 xx-go build -tags netgo -o /caddy/caddy cmd/caddy/main.go; \
    xx-verify --static /caddy/caddy

RUN echo "127.0.0.1 localhost" > /tmp/hosts

FROM scratch

COPY --from=build /tmp/hosts /etc/hosts
COPY --from=build /caddy/caddy /usr/bin/caddy
COPY ./rootfs/ /
