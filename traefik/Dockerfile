FROM --platform=$BUILDPLATFORM tonistiigi/xx:1.10.0 AS xx

FROM --platform=$BUILDPLATFORM node:14.16-stretch AS build-frontend

WORKDIR /

RUN set -xe; \
    wget -O traefik.tar.gz "https://github.com/traefik/traefik/archive/refs/tags/v2.10.6.tar.gz"; \
    tar xzvf traefik.tar.gz;

WORKDIR /traefik-2.10.6/webui

RUN set -xe; \
    yarn install; \
    yarn build

FROM --platform=$BUILDPLATFORM golang:1.21.4-alpine3.17 AS build-backend

COPY --from=xx / /

ARG TARGETPLATFORM

COPY --from=build-frontend /traefik-2.10.6 /traefik

WORKDIR /traefik

ENV TRAEFIK_CODENAME=saintmarcelin
ENV TRAEFIK_VERSION=2.10.6

RUN set -xe; \
    CGO_ENABLED=0 \
    xx-go build -v \
        -ldflags "-X 'github.com/traefik/traefik/v2/pkg/version.Version=${TRAEFIK_VERSION}' -X 'github.com/traefik/traefik/v2/pkg/version.Codename=${TRAEFIK_CODENAME}' -X 'github.com/traefik/traefik/v2/pkg/version.BuildDate=$(date)'" \
        -o /usr/bin/traefik \
        ./cmd/traefik; \
    xx-verify --static /usr/bin/traefik

FROM scratch

COPY --from=build-backend /usr/bin/traefik /usr/bin/traefik
COPY ./rootfs/ /
