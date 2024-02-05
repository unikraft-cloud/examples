FROM rust:1.75.0-bookworm AS spin

ARG SPIN_VERSION=2.1.0

WORKDIR /spin

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
      ca-certificates \
      make \
      wget;

RUN set -xe; \
    wget -q -O spin.tar.gz "https://github.com/fermyon/spin/releases/download/v${SPIN_VERSION}/spin-v${SPIN_VERSION}-linux-amd64.tar.gz"; \
    tar xzvf ./spin.tar.gz; \
    mv ./spin /usr/bin/spin; \
    rm -rf spin.tar.gz; \
    rustup target add wasm32-wasi

ARG WASI_SDK_VERSION=21

WORKDIR /wasi

RUN set -xe; \
    wget -q -O wasi-sdk.tar.gz "https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-${WASI_SDK_VERSION}/wasi-sdk-${WASI_SDK_VERSION}.0-linux.tar.gz"; \
    mkdir -p /opt/wasi-sdk; \
    tar xzvf ./wasi-sdk.tar.gz --strip-components 1 -C /opt/wasi-sdk/; \
    rm -rf ./wasi-sdk.tar.gz;

FROM spin AS build

COPY ./http-rust /app/http-rust
WORKDIR /app/http-rust
RUN cargo build --release

COPY ./wagi-http-cpp /app/wagi-http-cpp
WORKDIR /app/wagi-http-cpp
RUN make build

FROM scratch

COPY --from=build /app /app
COPY ./spin.toml /app/spin.toml
