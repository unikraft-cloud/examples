FROM nginx:1.25.3-bookworm AS build

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends pax-utils; \
    rm -rf /var/lib/apt/lists/*

RUN set -xe; \
    rm -f /var/log/nginx/access.log /var/log/nginx/error.log; \
    touch /var/log/nginx/access.log /var/log/nginx/error.log; \
    mkdir -p /rootfs/run /rootfs/tmp; \
    ln -s /usr/sbin/nginx /usr/bin/nginx; \
    lddtree --copy-to-tree /rootfs /usr/bin/nginx; \
    tar -C / -cf /tmp/data.tar etc/nginx etc/passwd etc/group var/log/nginx var/cache/nginx var/run; \
    tar -C /rootfs -xf /tmp/data.tar; \
    rm -f /rootfs/etc/nginx/modules; \
    find /rootfs -type d -exec chmod 755 {} +; \
    chmod 1777 /rootfs/tmp

COPY ./rootfs/ /rootfs/

RUN chroot /rootfs /usr/bin/nginx -t -c /etc/nginx/nginx.conf

FROM scratch

COPY --from=build /rootfs /
