FROM --platform=$BUILDPLATFORM node:23-bookworm AS build

WORKDIR /app

COPY . /app/

RUN set -xe; \
    npm ci; \
    npm run build

FROM nginx:1.25.3-bookworm AS rootfs

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends pax-utils; \
    rm -rf /var/lib/apt/lists/*

COPY ./rootfs/ /
COPY --from=build /app/dist /wwwroot

RUN set -xe; \
    rm -f /var/log/nginx/access.log /var/log/nginx/error.log; \
    touch /var/log/nginx/access.log /var/log/nginx/error.log; \
    mkdir -p /rootfs/tmp; \
    lddtree --copy-to-tree /rootfs /usr/sbin/nginx; \
    tar -C / -cf /tmp/data.tar etc/nginx etc/passwd etc/group var/log/nginx var/cache/nginx var/run run wwwroot; \
    tar -C /rootfs -xf /tmp/data.tar; \
    find /rootfs -type d -exec chmod 755 {} +; \
    chmod 1777 /rootfs/tmp; \
    chroot /rootfs /usr/sbin/nginx -t

FROM scratch

COPY --from=rootfs /rootfs /
