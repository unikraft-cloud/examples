FROM --platform=$BUILDPLATFORM node:14.16 AS build-frontend

WORKDIR /

RUN set -xe; \
    wget -O traefik.tar.gz "https://github.com/traefik/traefik/archive/refs/tags/v2.10.6.tar.gz"; \
    tar xzvf traefik.tar.gz;

WORKDIR /traefik-2.10.6/webui

# Build traefik frontend (architecture-independent)
RUN set -xe; \
    yarn install; \
    yarn build

FROM --platform=$BUILDPLATFORM golang:1.21.4-bookworm AS build-backend

ARG TARGETOS
ARG TARGETARCH

COPY --from=build-frontend /traefik-2.10.6 /traefik

WORKDIR /traefik

ENV TRAEFIK_CODENAME=saintmarcelin
ENV TRAEFIK_VERSION=2.10.6

# Cross-compile natively on the build host. -linkmode external requires a C
# toolchain for the target architecture, so install a cross toolchain when
# the build and target architectures differ.
RUN set -xe; \
    if [ "$(dpkg --print-architecture)" != "${TARGETARCH}" ]; then \
      apt-get update; \
      apt-get install -y --no-install-recommends crossbuild-essential-${TARGETARCH}; \
      case "${TARGETARCH}" in \
        amd64) export CC=x86_64-linux-gnu-gcc ;; \
        arm64) export CC=aarch64-linux-gnu-gcc ;; \
        *) echo "unsupported TARGETARCH: ${TARGETARCH}" >&2; exit 1 ;; \
      esac; \
    fi; \
    CGO_ENABLED=1 GOOS=${TARGETOS} GOARCH=${TARGETARCH} \
    go build -v \
        -buildmode=pie \
        -ldflags "-linkmode external -extldflags '-static-pie' -X 'github.com/traefik/traefik/v2/pkg/version.Version=${TRAEFIK_VERSION}' -X 'github.com/traefik/traefik/v2/pkg/version.Codename=${TRAEFIK_CODENAME}' -X 'github.com/traefik/traefik/v2/pkg/version.BuildDate=$(date)'" \
        -tags netgo \
        -o /usr/bin/traefik \
        ./cmd/traefik

FROM scratch

COPY --from=build-backend /usr/bin/traefik /usr/bin/traefik
COPY ./rootfs/ /
