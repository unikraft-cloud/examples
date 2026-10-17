FROM --platform=linux/x86_64 debian:bookworm AS wasmtime

ARG WASMTIME_VERSION=14.0.4

WORKDIR /wasmtime

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
      ca-certificates \
      wget \
      xz-utils; \
    wget https://github.com/bytecodealliance/wasmtime/releases/download/v${WASMTIME_VERSION}/wasmtime-v${WASMTIME_VERSION}-x86_64-linux.tar.xz; \
    tar xvf wasmtime-v${WASMTIME_VERSION}-x86_64-linux.tar.xz; \
    mv wasmtime-v${WASMTIME_VERSION}-x86_64-linux/wasmtime /usr/local/bin; \
    rm -rf wasmtime-v${WASMTIME_VERSION}-x86_64-linux*;

FROM --platform=linux/x86_64 golang:1.21.3-bookworm AS build

WORKDIR /src

COPY ./main.go /src/main.go

RUN set -xe; \
    GOOS=wasip1 GOARCH=wasm \
    go build \
      -o /main.wasm main.go \
    ;

FROM scratch

COPY --from=build /main.wasm /main.wasm
COPY --from=wasmtime /usr/local/bin/wasmtime /usr/local/bin/
COPY --from=wasmtime /lib/x86_64-linux-gnu/libdl.so.2 /lib/x86_64-linux-gnu/
COPY --from=wasmtime /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/
COPY --from=wasmtime /lib/x86_64-linux-gnu/librt.so.1 /lib/x86_64-linux-gnu/
COPY --from=wasmtime /lib/x86_64-linux-gnu/libpthread.so.0 /lib/x86_64-linux-gnu/
COPY --from=wasmtime /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/
COPY --from=wasmtime /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/
COPY --from=wasmtime /lib64/ld-linux-x86-64.so.2 /lib64/

