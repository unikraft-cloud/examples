FROM --platform=$BUILDPLATFORM golang:1.24.3-bookworm AS build

ARG TARGETOS
ARG TARGETARCH

WORKDIR /src

COPY ./src /src

# Cross-compile natively on the build host. cgo (DuckDB bindings) and
# -linkmode external require a C/C++ toolchain for the target architecture,
# so install a cross toolchain when the build and target architectures differ.
#
# Debian's cross libc ships libm.a as a linker script that references the
# static archives by their native multiarch path (/usr/lib/<triple>/), which
# does not exist in the cross sysroot (/usr/<triple>/lib/). Symlink the
# archives there so static -lm links resolve.
RUN set -xe; \
    if [ "$(dpkg --print-architecture)" != "${TARGETARCH}" ]; then \
      apt-get update; \
      apt-get install -y --no-install-recommends crossbuild-essential-${TARGETARCH}; \
      case "${TARGETARCH}" in \
        amd64) TRIPLE=x86_64-linux-gnu ;; \
        arm64) TRIPLE=aarch64-linux-gnu ;; \
        *) echo "unsupported TARGETARCH: ${TARGETARCH}" >&2; exit 1 ;; \
      esac; \
      export CC=${TRIPLE}-gcc CXX=${TRIPLE}-g++; \
      mkdir -p /usr/lib/${TRIPLE}; \
      ln -sf /usr/${TRIPLE}/lib/*.a /usr/lib/${TRIPLE}/; \
    fi; \
    CGO_ENABLED=1 GOOS=${TARGETOS} GOARCH=${TARGETARCH} \
    go build \
      -buildmode=pie \
      -ldflags "-linkmode external -extldflags -static-pie" \
      -tags netgo \
      -o /server /src/... \
    ;

FROM scratch

COPY --from=build /server /server
