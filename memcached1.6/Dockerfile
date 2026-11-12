FROM memcached:1.6-trixie AS build

USER root

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends pax-utils; \
    rm -rf /var/lib/apt/lists/*

RUN set -xe; \
    mkdir -p /rootfs/tmp; \
    ln -s /usr/local/bin/memcached /usr/bin/memcached; \
    lddtree --copy-to-tree /rootfs /usr/bin/memcached; \
    tar -C / -cf /tmp/data.tar etc/passwd; \
    tar -C /rootfs -xf /tmp/data.tar; \
    find /rootfs -type d -exec chmod 755 {} +; \
    chmod 1777 /rootfs/tmp; \
    chroot /rootfs /usr/bin/memcached --version

FROM scratch

COPY --from=build /rootfs /
