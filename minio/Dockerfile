FROM --platform=$BUILDPLATFORM golang:1.21.4-bookworm AS build

ARG TARGETOS
ARG TARGETARCH

ARG MINIO_VERSION=2024-02-04T22-36-13Z
ARG MINIO_COMMIT=f225ca331203032888889c1c4a3f96ee3452b9f9

RUN set -xe; \
    wget -q -O minio.tar.gz "https://github.com/minio/minio/archive/refs/tags/RELEASE.${MINIO_VERSION}.tar.gz"; \
    mkdir /minio; \
    tar xzvf ./minio.tar.gz --strip-components 1 -C /minio;

WORKDIR /minio

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
    COPYRIGHT_YEAR="${MINIO_VERSION%%-*}"; \
    SHORT_COMMIT_ID="$(echo "${MINIO_COMMIT}" | cut -c 1-12)"; \
    CGO_ENABLED=1 GOOS=${TARGETOS} GOARCH=${TARGETARCH} \
    go build -v \
        -buildmode=pie \
        -ldflags "-linkmode external -extldflags '-static-pie' -X github.com/minio/minio/cmd.Version=${MINIO_VERSION} -X github.com/minio/minio/cmd.CopyrightYear=${COPYRIGHT_YEAR} -X github.com/minio/minio/cmd.ReleaseTag=RELEASE.${MINIO_VERSION} -X github.com/minio/minio/cmd.CommitID=${MINIO_COMMIT} -X github.com/minio/minio/cmd.ShortCommitID=${SHORT_COMMIT_ID} -X github.com/minio/minio/cmd.GOPATH=/go -X github.com/minio/minio/cmd.GOROOT=" \
        -tags netgo \
        -o /usr/bin/minio \
        .

FROM scratch

COPY --from=build /usr/bin/minio /usr/bin/minio
