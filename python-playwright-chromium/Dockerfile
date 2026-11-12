FROM debian:bookworm AS build

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        fontconfig \
        libatomic1 \
        pax-utils \
        python3 \
        python3-venv \
    ; \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN set -xe; \
    python3 -m venv .venv; \
    . .venv/bin/activate; \
    pip install --no-cache-dir -r requirements.txt; \
    playwright install --with-deps --only-shell chromium; \
    rm -rf /var/lib/apt/lists/*

COPY ./main.py /app/main.py
COPY ./wrapper.sh /usr/bin/wrapper.sh

RUN set -xe; \
    mkdir -p /rootfs/tmp; \
    fc-cache -f; \
    lddtree --copy-to-tree /rootfs /usr/bin/python3 /bin/sh \
        /usr/lib/*/libsoftokn3.so /usr/lib/*/libfreeblpriv3.so /usr/lib/*/libnssckbi.so; \
    find /app /root/.cache/ms-playwright /usr/lib/python3.11 -type f -print0 \
        | xargs -0 lddtree --skip-non-elfs --copy-to-tree /rootfs; \
    tar -C / -cf /tmp/data.tar \
        app \
        root/.cache/ms-playwright \
        usr/bin/wrapper.sh \
        usr/lib/os-release \
        usr/lib/python3 \
        usr/lib/python3.11 \
        usr/lib/ssl/cert.pem \
        usr/lib/ssl/certs \
        usr/share/ca-certificates \
        usr/share/fontconfig \
        usr/share/fonts \
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
    chroot /rootfs /app/.venv/bin/python -c 'import fastapi, playwright.async_api, ssl; assert ssl.create_default_context().cert_store_stats()["x509_ca"]'; \
    chroot /rootfs /bin/sh -c '/root/.cache/ms-playwright/chromium_headless_shell-*/chrome-*/chrome-headless-shell --version'

FROM scratch

COPY --from=build /rootfs /
