FROM debian:bookworm-slim AS build

ARG HUGO_VERSION=0.160.0
ARG TARGETARCH

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends ca-certificates curl pax-utils; \
    curl -fsSL "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-${TARGETARCH}.tar.gz" \
      | tar -xz -C /usr/bin hugo; \
    rm -rf /var/lib/apt/lists/*

RUN set -xe; \
    install -d -m 1777 /rootfs/tmp; \
    lddtree --copy-to-tree /rootfs /usr/bin/hugo; \
    chroot /rootfs /usr/bin/hugo version

FROM scratch

COPY --from=build /rootfs /
COPY ./site /site
