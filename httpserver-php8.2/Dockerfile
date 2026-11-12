FROM php:8.2-cli-bookworm AS build

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends pax-utils

RUN docker-php-ext-install sockets

COPY ./rootfs/ /rootfs/

COPY ./server.php /rootfs/usr/src/server.php

RUN set -xe; \
    mkdir -p /rootfs/tmp; \
    lddtree --copy-to-tree /rootfs /usr/local/bin/php; \
    find /usr/local/lib/php -type f -print0 | xargs -0 lddtree --skip-non-elfs --copy-to-tree /rootfs; \
    tar -C / -cf /tmp/data.tar usr/local/lib/php; \
    tar -C /rootfs -xf /tmp/data.tar; \
    find /rootfs -type d -exec chmod 755 {} +; \
    chmod 1777 /rootfs/tmp; \
    chroot /rootfs /usr/local/bin/php -r 'exit(extension_loaded("sockets") ? 0 : 1);'

FROM scratch

COPY --from=build /rootfs /
