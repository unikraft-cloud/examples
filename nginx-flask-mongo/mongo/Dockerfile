FROM mongo:6.0.13-jammy AS build

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends pax-utils

RUN set -xe; \
    mkdir -p /rootfs/tmp; \
    lddtree -l /usr/bin/mongod | sort -u > /tmp/libs.txt; \
    tar -chf /tmp/libs.tar -T /tmp/libs.txt; \
    tar -C /rootfs -xf /tmp/libs.tar; \
    tar -C / -cf /tmp/data.tar etc/lsb-release data/db; \
    tar -C /rootfs -xf /tmp/data.tar; \
    find /rootfs -type d -exec chmod 755 {} +; \
    chmod 1777 /rootfs/tmp; \
    mkdir /rootfs/dev; \
    mknod /rootfs/dev/urandom c 1 9; \
    chroot /rootfs /usr/bin/mongod --version; \
    rm -r /rootfs/dev

FROM scratch

COPY --from=build /rootfs /
