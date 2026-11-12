FROM node:26-alpine3.24 AS build

RUN apk add --no-cache lddtree pax-utils

COPY ./server.js /usr/src/server.js

RUN set -xe; \
    mkdir -p /rootfs/tmp; \
    lddtree -l /usr/local/bin/node | sort -u > /tmp/libs.txt; \
    tar -cf /tmp/libs.tar -T /tmp/libs.txt; \
    tar -C /rootfs -xf /tmp/libs.tar; \
    tar -C / -cf /tmp/data.tar usr/src; \
    tar -C /rootfs -xf /tmp/data.tar; \
    chmod 1777 /rootfs/tmp; \
    chroot /rootfs /usr/local/bin/node -e 1

FROM scratch

COPY --from=build /rootfs /
