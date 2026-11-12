FROM mongo:6.0.13-jammy AS build

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends pax-utils; \
    rm -rf /var/lib/apt/lists/*

RUN set -xe; \
    mkdir -p -m 1777 /rootfs/tmp; \
    mkdir -p /rootfs/dev; \
    lddtree -l /usr/bin/mongod | sort -u > /tmp/libs.txt; \
    tar -chf /tmp/libs.tar -T /tmp/libs.txt; \
    tar -C /rootfs -xf /tmp/libs.tar; \
    tar -C / -chf /tmp/data.tar etc/lsb-release etc/localtime data/db; \
    tar -C /rootfs -xf /tmp/data.tar; \
    mknod -m 444 /rootfs/dev/urandom c 1 9; \
    chroot /rootfs /usr/bin/mongod --version; \
    rm /rootfs/dev/urandom

FROM scratch

COPY --from=build /rootfs /
