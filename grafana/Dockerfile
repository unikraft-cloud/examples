FROM --platform=$BUILDPLATFORM golang:1.21.4-bookworm AS grafana-build

ARG TARGETOS
ARG TARGETARCH

WORKDIR /grafana

# Sources
RUN set -xe; \
    wget -O /grafana.tar.gz https://github.com/grafana/grafana/archive/refs/tags/v10.2.2.tar.gz; \
    tar -xzvf /grafana.tar.gz --strip-components 1 -C /grafana \
    ;

# Build backend. Code generation runs natively on the build host; the go
# build cross-compiles to the target architecture. -linkmode external
# requires a C toolchain for the target architecture, so install a cross
# toolchain when the build and target architectures differ.
RUN set -xe; \
    make gen-go; \
    if [ "$(dpkg --print-architecture)" != "${TARGETARCH}" ]; then \
      apt-get update; \
      apt-get install -y --no-install-recommends crossbuild-essential-${TARGETARCH}; \
      case "${TARGETARCH}" in \
        amd64) export CC=x86_64-linux-gnu-gcc ;; \
        arm64) export CC=aarch64-linux-gnu-gcc ;; \
        *) echo "unsupported TARGETARCH: ${TARGETARCH}" >&2; exit 1 ;; \
      esac; \
    fi; \
    CGO_ENABLED=1 \
    GOOS=${TARGETOS} \
    GOARCH=${TARGETARCH} \
    go build -v \
      -buildmode=pie \
      -ldflags "-linkmode external -extldflags '-static-pie' -X 'main.version=10.2.2' -X 'main.commit=161e3ca' -X 'main.buildstamp=$(date)' -X 'main.buildBranch=main'" \
      -tags netgo \
      -o /usr/share/grafana/bin/grafana \
      ./pkg/cmd/grafana \
    ;

# Static assets (architecture-independent) from the upstream image.
FROM --platform=linux/x86_64 grafana/grafana:10.2.2 AS grafana

FROM scratch

COPY --from=grafana-build /usr/share/grafana/bin/grafana /usr/share/grafana/bin/grafana
COPY --from=grafana       /usr/share/grafana/public/ /usr/share/grafana/public/
COPY --from=grafana       /usr/share/grafana/conf/ /usr/share/grafana/conf/
