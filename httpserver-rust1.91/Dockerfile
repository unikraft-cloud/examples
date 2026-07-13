# Single-file compile: build natively on the build host, cross-compiling and
# installing a cross C toolchain (for linking) when the build and target
# architectures differ.
FROM --platform=$BUILDPLATFORM rust:1.91.0-bookworm AS build

ARG TARGETARCH

WORKDIR /src

COPY ./server.rs /src/server.rs

RUN set -xe; \
    case "${TARGETARCH}" in \
      amd64) RUST_TARGET=x86_64-unknown-linux-gnu; CROSS_GCC=x86_64-linux-gnu-gcc ;; \
      arm64) RUST_TARGET=aarch64-unknown-linux-gnu; CROSS_GCC=aarch64-linux-gnu-gcc ;; \
      *) echo "unsupported TARGETARCH: ${TARGETARCH}" >&2; exit 1 ;; \
    esac; \
    LINKER_FLAGS=""; \
    if [ "$(dpkg --print-architecture)" != "${TARGETARCH}" ]; then \
      rustup target add "${RUST_TARGET}"; \
      apt-get update; \
      apt-get install -y --no-install-recommends crossbuild-essential-${TARGETARCH}; \
      LINKER_FLAGS="-C linker=${CROSS_GCC}"; \
    fi; \
    rustc --target "${RUST_TARGET}" ${LINKER_FLAGS} -o /server /src/server.rs

# Source of the x86_64 system libraries copied into the final image.
FROM --platform=linux/x86_64 debian:bookworm-slim AS libs

FROM scratch

COPY --from=build /server /server
COPY --from=libs /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/
COPY --from=libs /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/
COPY --from=libs /lib64/ld-linux-x86-64.so.2 /lib64/
