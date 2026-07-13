FROM --platform=$BUILDPLATFORM golang:1.21.3-bookworm AS build

ARG CADDY_VERSION=2.7.6
ARG TARGETOS
ARG TARGETARCH

WORKDIR /caddy

# Cross-compile natively on the build host. -linkmode external requires a C
# toolchain for the target architecture, so install a cross toolchain when
# the build and target architectures differ.
RUN --mount=type=cache,target=/root/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
      git; \
    if [ "$(dpkg --print-architecture)" != "${TARGETARCH}" ]; then \
      apt-get install -y --no-install-recommends crossbuild-essential-${TARGETARCH}; \
      case "${TARGETARCH}" in \
        amd64) export CC=x86_64-linux-gnu-gcc ;; \
        arm64) export CC=aarch64-linux-gnu-gcc ;; \
        *) echo "unsupported TARGETARCH: ${TARGETARCH}" >&2; exit 1 ;; \
      esac; \
    fi; \
    git clone --depth=1 --branch v${CADDY_VERSION} https://github.com/caddyserver/caddy.git /caddy; \
    CGO_ENABLED=1 GOOS=${TARGETOS} GOARCH=${TARGETARCH} \
    go build \
      -buildmode=pie \
      -ldflags "-linkmode external -extldflags -static-pie" \
      -tags netgo \
      -o /caddy/caddy cmd/caddy/main.go;

RUN echo "127.0.0.1 localhost" > /tmp/hosts

FROM scratch

COPY --from=build /tmp/hosts /etc/hosts
COPY --from=build /caddy/caddy /usr/bin/caddy
COPY ./rootfs/ /
