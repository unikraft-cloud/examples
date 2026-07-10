FROM --platform=$BUILDPLATFORM golang:1.21.4-alpine3.17 AS build

RUN set -xe; \
    apk --no-cache add \
      gcc \
      musl-dev \
      wget \
      ca-certificates \
    ; \
    update-ca-certificates;

ARG MINIO_VERSION=2024-02-04T22-36-13Z
ARG MINIO_COMMIT=f225ca331203032888889c1c4a3f96ee3452b9f9

RUN set -xe; \
    wget -q -O minio.tar.gz "https://github.com/minio/minio/archive/refs/tags/RELEASE.${MINIO_VERSION}.tar.gz"; \
    mkdir /minio; \
    tar xzvf ./minio.tar.gz --strip-components 1 -C /minio;

WORKDIR /minio

RUN set -xe; \
    CGO_ENABLED=1 \
    go build -v \
        -buildmode=pie \
        -ldflags "-linkmode external -extldflags '-static-pie' -X github.com/minio/minio/cmd.Version=${MINIO_VERSION} -X github.com/minio/minio/cmd.CopyrightYear=${MINIO_VERSION:0:4} -X github.com/minio/minio/cmd.ReleaseTag=RELEASE.${MINIO_VERSION} -X github.com/minio/minio/cmd.CommitID=${MINIO_COMMIT} -X github.com/minio/minio/cmd.ShortCommitID=${MINIO_COMMIT:0:12} -X github.com/minio/minio/cmd.GOPATH=/go -X github.com/minio/minio/cmd.GOROOT=" \
        -o /usr/bin/minio \
        .

FROM --platform=$BUILDPLATFORM scratch

COPY --from=build /usr/bin/minio /usr/bin/minio
