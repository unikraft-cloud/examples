FROM haproxy:2.8.3-alpine3.18 AS build

USER root

RUN apk add --no-cache lddtree pax-utils

COPY ./rootfs/ /rootfs/

RUN set -xe; \
    mkdir -p -m 1777 /rootfs/tmp; \
    ln -s /usr/local/sbin/haproxy /usr/bin/haproxy; \
    lddtree -l /usr/bin/haproxy | sort -u > /tmp/libs.txt; \
    tar -cf /tmp/libs.tar -T /tmp/libs.txt; \
    tar -C /rootfs -xf /tmp/libs.tar; \
    tar -C / -cf /tmp/data.tar usr/local/etc/haproxy; \
    tar -C /rootfs -xf /tmp/data.tar; \
    chroot /rootfs /usr/bin/haproxy -c -f /etc/haproxy/haproxy.conf

FROM scratch

COPY --from=build /rootfs /
