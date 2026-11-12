FROM oven/bun:1.4.4-alpine AS build

RUN apk add --no-cache lddtree pax-utils

COPY ./server.ts /usr/src/server.ts

RUN set -xe; \
    mkdir -p /rootfs/tmp; \
    lddtree -l /usr/local/bin/bun | sort -u > /tmp/libs.txt; \
    tar -cf /tmp/libs.tar -T /tmp/libs.txt; \
    tar -C /rootfs -xf /tmp/libs.tar; \
    tar -C / -cf /tmp/data.tar usr/src; \
    tar -C /rootfs -xf /tmp/data.tar; \
    chmod 1777 /rootfs/tmp; \
    chroot /rootfs /usr/local/bin/bun --version

FROM scratch

COPY --from=build /rootfs /
