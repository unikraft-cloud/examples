FROM node:22-bookworm-slim AS build

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends ca-certificates fontconfig pax-utils; \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY package.json package-lock.json /app/

RUN set -xe; \
    PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm ci --omit=dev; \
    npx playwright install --with-deps webkit; \
    rm -rf /var/lib/apt/lists/*

COPY ./server.js /app/server.js
COPY ./wrapper.sh /usr/bin/wrapper.sh

RUN set -xe; \
    mkdir -p /rootfs/tmp; \
    fc-cache -f; \
    lddtree --copy-to-tree /rootfs /usr/local/bin/node /bin/sh /bin/bash \
        /usr/bin/dirname /usr/bin/env /usr/bin/readlink /usr/bin/uname \
        /usr/lib/*/libEGL_mesa.so.0 /usr/lib/*/libGLESv2.so.2 /usr/lib/*/dri/swrast_dri.so \
        /usr/lib/*/gio/modules/libgiognutls.so; \
    find /app /root/.cache/ms-playwright -type f -print0 \
        | xargs -0 lddtree --skip-non-elfs --copy-to-tree /rootfs; \
    tar -C / -cf /tmp/data.tar \
        app \
        root/.cache/ms-playwright \
        usr/bin/wrapper.sh \
        usr/lib/os-release \
        usr/share/fontconfig \
        usr/share/fonts \
        usr/share/glvnd \
        var/cache/fontconfig \
        etc/fonts \
        etc/group \
        etc/nsswitch.conf \
        etc/os-release \
        etc/passwd \
        etc/ssl/certs \
    ; \
    tar -C /rootfs -xf /tmp/data.tar; \
    printf '127.0.0.1 localhost\n::1 localhost\n' > /rootfs/etc/hosts; \
    find /rootfs -type d -exec chmod 755 {} +; \
    chmod 1777 /rootfs/tmp; \
    chroot /rootfs /usr/local/bin/node -e 'require("/app/node_modules/playwright")'; \
    chroot /rootfs /bin/sh -c '/root/.cache/ms-playwright/webkit-*/pw_run.sh --headless --version'

FROM scratch

COPY --from=build /rootfs /
