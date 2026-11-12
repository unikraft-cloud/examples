FROM node:25-bookworm-slim AS build

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends pax-utils; \
    rm -rf /var/lib/apt/lists/*

WORKDIR /src

COPY package.json package-lock.json ./

RUN npm ci --omit=dev

COPY ./server.ts ./

RUN set -xe; \
    mkdir -p /rootfs/tmp /rootfs/run; \
    lddtree --copy-to-tree /rootfs /usr/local/bin/node; \
    find /src -type f -print0 | xargs -0 lddtree --skip-non-elfs --copy-to-tree /rootfs; \
    tar -C / -cf /tmp/data.tar src; \
    tar -C /rootfs -xf /tmp/data.tar; \
    find /rootfs -type d -exec chmod 755 {} +; \
    chmod 1777 /rootfs/tmp; \
    chroot /rootfs /usr/local/bin/node -e 1

FROM scratch

COPY --from=build /rootfs /
