FROM --platform=$BUILDPLATFORM node:24-bookworm-slim AS build

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
      ca-certificates \
      git \
    ; \
    corepack enable pnpm

WORKDIR /allkaraoke

RUN set -xe; \
    git init -q; \
    git fetch -q --depth=1 https://github.com/Asvarox/allkaraoke.git 9587d6daad5abc6bda1a2a90720652fb3f42d032; \
    git checkout -q FETCH_HEAD; \
    pnpm install --frozen-lockfile; \
    pnpm exec playwright install --with-deps chromium; \
    pnpm build

FROM node:24-bookworm-slim AS rootfs

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends pax-utils; \
    rm -rf /var/lib/apt/lists/*; \
    npm install -g serve@14.2.7

COPY --from=build /allkaraoke/build/client /wwwroot
COPY ./entrypoint.sh /entrypoint.sh

RUN set -xe; \
    mkdir -p /rootfs/tmp; \
    lddtree --copy-to-tree /rootfs /usr/local/bin/node /bin/sh; \
    find /usr/local/lib/node_modules/serve -type f -print0 | xargs -0 lddtree --skip-non-elfs --copy-to-tree /rootfs; \
    tar -C / -cf /tmp/data.tar usr/local/lib/node_modules/serve wwwroot entrypoint.sh; \
    tar -C /rootfs -xf /tmp/data.tar; \
    find /rootfs -type d -exec chmod 755 {} +; \
    chmod 1777 /rootfs/tmp; \
    chroot /rootfs /bin/sh -c 'exec node /usr/local/lib/node_modules/serve/build/main.js --version'

FROM scratch

COPY --from=rootfs /rootfs /
