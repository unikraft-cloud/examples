FROM redis:7.2-bookworm AS build

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends pax-utils; \
    rm -rf /var/lib/apt/lists/*

RUN set -xe; \
    mkdir -p /rootfs/tmp; \
    ln -s /usr/local/bin/redis-server /usr/bin/redis-server; \
    lddtree --copy-to-tree /rootfs /usr/bin/redis-server; \
    find /rootfs -type d -exec chmod 755 {} +; \
    chmod 1777 /rootfs/tmp; \
    chroot /rootfs /usr/bin/redis-server --version

FROM scratch

COPY --from=build /rootfs /
COPY ./fs/ /
