FROM --platform=$BUILDPLATFORM golang:1.21.6-bookworm AS build

ARG TARGETOS
ARG TARGETARCH

WORKDIR /src

COPY ./age-calculator.go /src/age-calculator.go
COPY ./go.mod /src/go.mod
COPY ./go.sum /src/go.sum
COPY ./testdata /src/testdata

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
    go build -v \
      -buildmode=pie \
      -ldflags "-linkmode external -extldflags -static-pie" \
      -tags netgo \
      -o /age-calculator age-calculator.go \
    ;

FROM scratch

COPY --from=build /age-calculator /age-calculator
