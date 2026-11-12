FROM docker.dragonflydb.io/dragonflydb/dragonfly:v1.14.1 AS build

USER root

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends pax-utils; \
    rm -rf /var/lib/apt/lists/*

RUN set -xe; \
    mkdir -p -m 1777 /rootfs/tmp; \
    ln -s /usr/local/bin/dragonfly /usr/bin/dragonfly; \
    lddtree -l /usr/bin/dragonfly /bin/bash /usr/bin/mount /usr/bin/mkdir | sort -u > /tmp/libs.txt; \
    tar -chf /tmp/libs.tar -T /tmp/libs.txt; \
    tar -C /rootfs -xf /tmp/libs.tar; \
    chroot /rootfs /usr/bin/dragonfly --version; \
    chroot /rootfs /bin/bash -c '/usr/bin/mount --version && /usr/bin/mkdir --version'

FROM scratch

COPY --from=build /rootfs /
COPY ./wrapper.sh /usr/bin/wrapper.sh
