FROM redis:7.2.2-bookworm AS build

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends pax-utils; \
    rm -rf /var/lib/apt/lists/*

RUN set -xe; \
    install -d -m 1777 /rootfs/tmp; \
    ln -s /usr/local/bin/redis-server /usr/bin/redis-server; \
    lddtree --copy-to-tree /rootfs /usr/bin/redis-server /bin/sh; \
    chroot /rootfs /usr/bin/redis-server --version; \
    chroot /rootfs /bin/sh -c true

FROM scratch

COPY --from=build /rootfs /
COPY ./rootfs/ /
