# Build the wasm components natively on the build host — wasm is
# architecture-independent. spin and the WASI SDK run on the build host, so
# fetch them for its architecture; the amd64 spin binary that ships in the
# final image is downloaded separately.
FROM --platform=$BUILDPLATFORM rust:1.95.0-bookworm AS spin-devenv

ARG SPIN_VERSION=4.0.0

WORKDIR /spin

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
      ca-certificates \
      make \
      wget;

RUN set -xe; \
    case "$(dpkg --print-architecture)" in \
      amd64) SPIN_ARCH=amd64 ;; \
      arm64) SPIN_ARCH=aarch64 ;; \
      *) echo "unsupported build architecture" >&2; exit 1 ;; \
    esac; \
    wget -q -O spin.tar.gz "https://github.com/fermyon/spin/releases/download/v${SPIN_VERSION}/spin-v${SPIN_VERSION}-linux-${SPIN_ARCH}.tar.gz"; \
    tar xzvf ./spin.tar.gz; \
    mv ./spin /usr/bin/spin; \
    rm -rf spin.tar.gz; \
    wget -q -O spin-amd64.tar.gz "https://github.com/fermyon/spin/releases/download/v${SPIN_VERSION}/spin-v${SPIN_VERSION}-linux-amd64.tar.gz"; \
    mkdir -p /spin-dist; \
    tar xzf ./spin-amd64.tar.gz -C /spin-dist; \
    rm -rf spin-amd64.tar.gz; \
    rustup target add wasm32-wasip1

ARG WASI_SDK_VERSION=25

WORKDIR /wasi

RUN set -xe; \
    case "$(dpkg --print-architecture)" in \
      amd64) WASI_SDK_ARCH=x86_64 ;; \
      arm64) WASI_SDK_ARCH=arm64 ;; \
      *) echo "unsupported build architecture" >&2; exit 1 ;; \
    esac; \
    wget -q -O wasi-sdk.tar.gz "https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-${WASI_SDK_VERSION}/wasi-sdk-${WASI_SDK_VERSION}.0-${WASI_SDK_ARCH}-linux.tar.gz"; \
    mkdir -p /opt/wasi-sdk; \
    tar xzvf ./wasi-sdk.tar.gz --strip-components 1 -C /opt/wasi-sdk/; \
    rm -rf ./wasi-sdk.tar.gz;

FROM spin-devenv AS build

COPY ./hello-cpp /app/hello-cpp
COPY ./goodbye-rust /app/goodbye-rust
COPY ./spin.toml /app/spin.toml

WORKDIR /app

RUN spin build

# x86_64 system libraries for the final image (copy-only, nothing runs under
# emulation).
FROM --platform=linux/x86_64 debian:bookworm-slim AS libs

FROM scratch

# Binary executable
COPY --from=build /spin-dist/spin /usr/bin/spin

# System libraries
COPY --from=libs /lib/x86_64-linux-gnu/libstdc++.so.6 /lib/x86_64-linux-gnu/libstdc++.so.6
COPY --from=libs /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=libs /lib/x86_64-linux-gnu/librt.so.1 /lib/x86_64-linux-gnu/librt.so.1
COPY --from=libs /lib/x86_64-linux-gnu/libpthread.so.0 /lib/x86_64-linux-gnu/libpthread.so.0
COPY --from=libs /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=libs /lib/x86_64-linux-gnu/libdl.so.2 /lib/x86_64-linux-gnu/libdl.so.2
COPY --from=libs /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=libs /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2

# CA certificates required by Spin for TLS initialization
COPY --from=build /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

COPY ./spin.toml /app/spin.toml
COPY --from=build /app/hello-cpp/hello.wasm /app/hello-cpp/hello.wasm
COPY --from=build /app/goodbye-rust/target/wasm32-wasip1/release/goodbye.wasm /app/goodbye-rust/target/wasm32-wasip1/release/goodbye.wasm
