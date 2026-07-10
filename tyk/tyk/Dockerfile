FROM --platform=$BUILDPLATFORM golang:1.21.3-bookworm AS build

ARG TYK_VERSION=5.2.6

WORKDIR /tyk

RUN --mount=type=cache,target=/root/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
      git; \
    git clone --depth=1 --branch v${TYK_VERSION} https://github.com/TykTechnologies/tyk /tyk; \
    go build  \
      -buildmode=pie \
      -ldflags "-linkmode external -extldflags -static-pie" \
      -tags netgo;

FROM --platform=$BUILDPLATFORM scratch

COPY --from=build /tyk/tyk /usr/bin/tyk
COPY --from=build /tyk/templates /tyk/templates

COPY ./rootfs/ /
