ARG SPIN_VERSION=4.0.0

FROM --platform=$BUILDPLATFORM rust:1.95.0-bookworm AS spin-devenv

ARG SPIN_VERSION
ARG BUILDARCH

WORKDIR /spin

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
      ca-certificates \
      make \
      wget;

RUN set -xe; \
    case "$BUILDARCH" in \
      amd64) spin_arch=amd64 ;; \
      arm64) spin_arch=aarch64 ;; \
      *) echo "unsupported architecture: $BUILDARCH" >&2; exit 1 ;; \
    esac; \
    wget -q -O spin.tar.gz "https://github.com/fermyon/spin/releases/download/v${SPIN_VERSION}/spin-v${SPIN_VERSION}-linux-${spin_arch}.tar.gz"; \
    tar xzvf ./spin.tar.gz; \
    mv ./spin /usr/bin/spin; \
    rm -rf spin.tar.gz; \
    rustup target add wasm32-wasip1

ARG WASI_SDK_VERSION=23

WORKDIR /wasi

RUN set -xe; \
    case "$BUILDARCH" in \
      amd64) wasi_arch=x86_64 ;; \
      arm64) wasi_arch=arm64 ;; \
      *) echo "unsupported architecture: $BUILDARCH" >&2; exit 1 ;; \
    esac; \
    wget -q -O wasi-sdk.tar.gz "https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-${WASI_SDK_VERSION}/wasi-sdk-${WASI_SDK_VERSION}.0-${wasi_arch}-linux.tar.gz"; \
    mkdir -p /opt/wasi-sdk; \
    tar xzvf ./wasi-sdk.tar.gz --strip-components 1 -C /opt/wasi-sdk/; \
    rm -rf ./wasi-sdk.tar.gz;

FROM spin-devenv AS build

COPY ./hello-cpp /app/hello-cpp
COPY ./goodbye-rust /app/goodbye-rust
COPY ./spin.toml /app/spin.toml

WORKDIR /app

RUN spin build

FROM debian:bookworm-slim AS spin

ARG SPIN_VERSION
ARG TARGETARCH

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends ca-certificates pax-utils wget; \
    case "$TARGETARCH" in \
      amd64) spin_arch=amd64 ;; \
      arm64) spin_arch=aarch64 ;; \
      *) echo "unsupported architecture: $TARGETARCH" >&2; exit 1 ;; \
    esac; \
    wget -q -O - "https://github.com/fermyon/spin/releases/download/v${SPIN_VERSION}/spin-v${SPIN_VERSION}-linux-${spin_arch}.tar.gz" \
      | tar -xz -C /usr/bin spin; \
    install -d -m 1777 /rootfs/tmp; \
    lddtree --copy-to-tree /rootfs /usr/bin/spin; \
    tar -C / -cf /tmp/data.tar etc/ssl/certs/ca-certificates.crt; \
    tar -C /rootfs -xf /tmp/data.tar; \
    chroot /rootfs /usr/bin/spin --version

FROM scratch

COPY --from=spin /rootfs /

COPY ./spin.toml /app/spin.toml
COPY --from=build /app/hello-cpp/hello.wasm /app/hello-cpp/hello.wasm
COPY --from=build /app/goodbye-rust/target/wasm32-wasip1/release/goodbye.wasm /app/goodbye-rust/target/wasm32-wasip1/release/goodbye.wasm
