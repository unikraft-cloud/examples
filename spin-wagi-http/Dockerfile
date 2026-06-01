FROM rust:1.95.0-bookworm AS spin-devenv

ARG SPIN_VERSION=4.0.0

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
    rustup target add wasm32-wasip1

ARG WASI_SDK_VERSION=21

WORKDIR /wasi

RUN set -xe; \
    wget -q -O wasi-sdk.tar.gz "https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-${WASI_SDK_VERSION}/wasi-sdk-${WASI_SDK_VERSION}.0-linux.tar.gz"; \
    mkdir -p /opt/wasi-sdk; \
    tar xzvf ./wasi-sdk.tar.gz --strip-components 1 -C /opt/wasi-sdk/; \
    rm -rf ./wasi-sdk.tar.gz;

FROM spin-devenv AS build

COPY ./hello-cpp /app/hello-cpp
COPY ./goodbye-rust /app/goodbye-rust
COPY ./spin.toml /app/spin.toml

WORKDIR /app

RUN spin build

FROM golang:1.22-bookworm AS launcher-build

WORKDIR /src
COPY ./launcher/launcher.go ./launcher.go
RUN CGO_ENABLED=0 go build -ldflags='-s -w' -o /launcher ./launcher.go

FROM scratch

# Launcher: waits for spin to bind, then writes /uk/libukp/template_instance
# when TEMPLATE=1 so UKC can snapshot for template-based warm restores.
COPY --from=launcher-build /launcher /launcher

# Binary executable
COPY --from=build /usr/bin/spin /usr/bin/spin

# System libraries
COPY --from=build /lib/x86_64-linux-gnu/libstdc++.so.6 /lib/x86_64-linux-gnu/libstdc++.so.6
COPY --from=build /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=build /lib/x86_64-linux-gnu/librt.so.1 /lib/x86_64-linux-gnu/librt.so.1
COPY --from=build /lib/x86_64-linux-gnu/libpthread.so.0 /lib/x86_64-linux-gnu/libpthread.so.0
COPY --from=build /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=build /lib/x86_64-linux-gnu/libdl.so.2 /lib/x86_64-linux-gnu/libdl.so.2
COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2

# CA certificates required by Spin for TLS initialization
COPY --from=build /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

COPY ./spin.toml /app/spin.toml
COPY --from=build /app/hello-cpp/hello.wasm /app/hello-cpp/hello.wasm
COPY --from=build /app/goodbye-rust/target/wasm32-wasip1/release/goodbye.wasm /app/goodbye-rust/target/wasm32-wasip1/release/goodbye.wasm
