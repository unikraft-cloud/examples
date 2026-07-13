FROM --platform=$BUILDPLATFORM golang:1.21.4-bookworm AS build

ARG TARGETOS
ARG TARGETARCH

RUN set -xe; apt-get update ; \
    apt-get install -y --no-install-recommends \
      build-essential \
      git \
    ;

WORKDIR /

RUN set -xe; \
    wget -O skipper.tar.gz "https://github.com/zalando/skipper/archive/refs/tags/v0.18.51.tar.gz"; \
    tar xzvf skipper.tar.gz;

WORKDIR /skipper-0.18.51

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
    go build \
        -buildmode=pie \
        -ldflags "-linkmode external -extldflags '-static-pie'" \
        -o /usr/bin/skipper \
        ./cmd/skipper

FROM scratch

COPY --from=build /usr/bin/skipper /usr/bin/skipper
COPY ./rootfs/ /
