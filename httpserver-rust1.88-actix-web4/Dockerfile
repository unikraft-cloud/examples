FROM --platform=$BUILDPLATFORM rust:1.88.0-bookworm AS build

ARG TARGETARCH

RUN cargo new --bin app
WORKDIR /app
COPY Cargo.toml ./
COPY Cargo.lock ./
COPY src ./src

# Cross-compile natively on the build host, installing the Rust target and a
# cross C toolchain (for linking) when the build and target architectures
# differ.
RUN set -xe; \
    case "${TARGETARCH}" in \
      amd64) RUST_TARGET=x86_64-unknown-linux-gnu ;; \
      arm64) RUST_TARGET=aarch64-unknown-linux-gnu ;; \
      *) echo "unsupported TARGETARCH: ${TARGETARCH}" >&2; exit 1 ;; \
    esac; \
    if [ "$(dpkg --print-architecture)" != "${TARGETARCH}" ]; then \
      rustup target add "${RUST_TARGET}"; \
      apt-get update; \
      apt-get install -y --no-install-recommends crossbuild-essential-${TARGETARCH}; \
      export CARGO_TARGET_X86_64_UNKNOWN_LINUX_GNU_LINKER=x86_64-linux-gnu-gcc; \
      export CARGO_TARGET_AARCH64_UNKNOWN_LINUX_GNU_LINKER=aarch64-linux-gnu-gcc; \
    fi; \
    cargo build --release --target "${RUST_TARGET}"; \
    cp "/app/target/${RUST_TARGET}/release/hello" /server

# Source of the x86_64 system libraries copied into the final image.
FROM --platform=linux/x86_64 debian:bookworm-slim AS libs

FROM scratch

COPY --from=build /server /server
COPY --from=libs /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/
COPY --from=libs /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/
COPY --from=libs /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/
COPY --from=libs /lib64/ld-linux-x86-64.so.2 /lib64/
