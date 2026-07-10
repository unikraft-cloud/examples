FROM --platform=$BUILDPLATFORM node:14.16 AS build-frontend

WORKDIR /

RUN set -xe; \
    wget -O traefik.tar.gz "https://github.com/traefik/traefik/archive/refs/tags/v2.10.6.tar.gz"; \
    tar xzvf traefik.tar.gz;

WORKDIR /traefik-2.10.6/webui

# Build traefik frontend
RUN set -xe; \
    yarn install; \
    yarn build

FROM --platform=$BUILDPLATFORM golang:1.21.4-alpine3.17 AS build-backend

RUN set -xe; \
    apk --no-cache add \
      gcc \
      musl-dev \
    ;

COPY --from=build-frontend /traefik-2.10.6 /traefik

WORKDIR /traefik

ENV TRAEFIK_CODENAME=saintmarcelin
ENV TRAEFIK_VERSION=2.10.6

RUN set -xe; \
    CGO_ENABLED=1 \
    go build -v \
        -buildmode=pie \
        -ldflags "-linkmode external -extldflags '-static-pie' -X 'github.com/traefik/traefik/v2/pkg/version.Version=${TRAEFIK_VERSION}' -X 'github.com/traefik/traefik/v2/pkg/version.Codename=${TRAEFIK_CODENAME}' -X 'github.com/traefik/traefik/v2/pkg/version.BuildDate=$(date)'" \
        -o /usr/bin/traefik \
        ./cmd/traefik

FROM --platform=$BUILDPLATFORM scratch

COPY --from=build-backend /usr/bin/traefik /usr/bin/traefik
COPY ./rootfs/ /
