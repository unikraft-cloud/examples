FROM node:22-bookworm-slim AS build

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends fontconfig pax-utils; \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY package.json package-lock.json /app/

RUN set -xe; \
    PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm ci --omit=dev; \
    npx playwright install --with-deps --only-shell chromium; \
    rm -rf /var/lib/apt/lists/*

COPY ./proxy.js /app/proxy.js
COPY ./wrapper.sh /usr/bin/wrapper.sh

RUN set -xe; \
    mkdir -p /rootfs/tmp /rootfs/app/data; \
    fc-cache -f; \
    lddtree --copy-to-tree /rootfs /usr/local/bin/node /bin/sh \
        /usr/lib/*/libsoftokn3.so /usr/lib/*/libfreeblpriv3.so /usr/lib/*/libnssckbi.so; \
    find /app /root/.cache/ms-playwright -type f -print0 \
        | xargs -0 lddtree --skip-non-elfs --copy-to-tree /rootfs; \
    tar -C / -cf /tmp/data.tar \
        app \
        root/.cache/ms-playwright \
        usr/bin/wrapper.sh \
        usr/lib/os-release \
        usr/share/fontconfig \
        usr/share/fonts \
        var/cache/fontconfig \
        etc/fonts \
        etc/group \
        etc/nsswitch.conf \
        etc/os-release \
        etc/passwd \
    ; \
    tar -C /rootfs -xf /tmp/data.tar; \
    printf '127.0.0.1 localhost\n::1 localhost\n' > /rootfs/etc/hosts; \
    find /rootfs -type d -exec chmod 755 {} +; \
    chmod 1777 /rootfs/tmp; \
    chroot /rootfs /usr/local/bin/node -e 'require("/app/node_modules/playwright"); new (require("/app/node_modules/better-sqlite3"))(":memory:")'; \
    shell=$(find /rootfs/root/.cache/ms-playwright -type f -executable -name '*shell'); \
    chroot /rootfs "${shell#/rootfs}" --version

FROM scratch

COPY --from=build /rootfs /
