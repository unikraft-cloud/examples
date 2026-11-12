FROM nginx:1.29.0-alpine3.22 AS build

RUN apk add --no-cache lddtree

COPY ./nginx.conf /rootfs/etc/nginx/nginx.conf.template
COPY ./entrypoint.sh /rootfs/entrypoint.sh

RUN set -xe; \
    mkdir -p /rootfs/tmp; \
    lddtree -l /usr/sbin/nginx /bin/sh /usr/bin/env /usr/bin/envsubst | sort -u > /tmp/libs.txt; \
    tar -cf /tmp/libs.tar -T /tmp/libs.txt; \
    tar -C /rootfs -xf /tmp/libs.tar; \
    tar -C / -cf /tmp/data.tar etc/passwd etc/group run var/run var/cache/nginx var/log/nginx; \
    tar -C /rootfs -xf /tmp/data.tar; \
    find /rootfs -type d -exec chmod 755 {} +; \
    chmod 1777 /rootfs/tmp; \
    chroot /rootfs /usr/bin/env sh -c 'envsubst --version && nginx -V'

FROM scratch

COPY --from=build /rootfs /
