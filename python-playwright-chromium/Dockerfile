# Everything in the final rootfs is a prebuilt x86_64 artifact, so each
# stage fetches and unpacks with native tools regardless of build host:
# Debian packages are unpacked by native dpkg via multiarch, Python
# wheels are downloaded for x86_64 with pip --platform, and Playwright's
# headless Chromium build is downloaded straight from its CDN.

# x86_64 Debian packages, unpacked natively via dpkg multiarch.
FROM --platform=$BUILDPLATFORM debian:bookworm AS debs

RUN set -xe; \
    dpkg --add-architecture amd64; \
    apt-get -yqq update; \
    apt-get -yqq install --no-install-recommends \
        # Chromium runtime dependencies
        libasound2:amd64 \
        libatk-bridge2.0-0:amd64 \
        libatk1.0-0:amd64 \
        libatspi2.0-0:amd64 \
        libcairo2:amd64 \
        libcups2:amd64 \
        libdbus-1-3:amd64 \
        libdrm2:amd64 \
        libfontconfig1:amd64 \
        libgbm1:amd64 \
        libglib2.0-0:amd64 \
        libnspr4:amd64 \
        libnss3:amd64 \
        libpango-1.0-0:amd64 \
        libstdc++6:amd64 \
        libudev1:amd64 \
        libx11-6:amd64 \
        libxcb1:amd64 \
        libxcomposite1:amd64 \
        libxdamage1:amd64 \
        libxext6:amd64 \
        libxfixes3:amd64 \
        libxi6:amd64 \
        libxkbcommon0:amd64 \
        libxrandr2:amd64 \
        fonts-dejavu-core \
        ca-certificates \
        # Python runtime, and ps which Playwright uses at runtime
        python3:amd64 \
        procps:amd64; \
    # python-is-python3 is arch:all, so apt resolves its python3 dependency
    # against the build host's native arch, which cannot coexist with
    # python3:amd64; it only ships the /usr/bin/python symlink, so create
    # that directly
    ln -s python3 /usr/bin/python; \
    # dash:amd64 conflicts with the build host's essential dash, so
    # unpack it manually to provide the rootfs /bin/sh
    cd /tmp; \
    apt-get -q download dash:amd64; \
    dpkg-deb -x dash_*.deb /dash-amd64; \
    mkdir /home/tmp

# x86_64 Python wheels and Chromium, fetched by native python/curl.
# debian:bookworm has the same python3.11 the rootfs gets from apt.
FROM --platform=$BUILDPLATFORM debian:bookworm AS pyapps

RUN set -xe; \
    apt-get -yqq update; \
    apt-get -yqq install --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        curl \
        unzip

WORKDIR /app
COPY ./requirements.txt .

# A venv would buy nothing in a single-workload rootfs: packages go
# straight into the path Debian's python already searches, and the CLI
# scripts pip generates get the /usr/bin/python3 shebang that matches
# the interpreter shipped in the final image.
RUN set -xe; \
    pip3 install --break-system-packages --no-cache-dir --only-binary=:all: \
        --platform manylinux1_x86_64 \
        --platform manylinux2010_x86_64 \
        --platform manylinux2014_x86_64 \
        --platform manylinux_2_17_x86_64 \
        --platform manylinux_2_24_x86_64 \
        --platform manylinux_2_28_x86_64 \
        --platform manylinux_2_31_x86_64 \
        --platform manylinux_2_34_x86_64 \
        --platform manylinux_2_35_x86_64 \
        --python-version 311 --implementation cp --abi cp311 \
        --target /x86-dist-packages \
        -r requirements.txt; \
    mkdir /x86-bin; \
    mv /x86-dist-packages/bin/* /x86-bin/; \
    # bytecode is arch-independent; precompile since the rootfs is read-only
    python3 -m compileall -q /x86-dist-packages || true

# main.py only launches headless Chromium, so only the headless-shell
# build is installed. URL layout matches what `playwright install
# --dry-run chromium-headless-shell` prints for the pinned version.
RUN set -xe; \
    BROWSERS=/x86-dist-packages/playwright/driver/package/browsers.json; \
    JSONQ="import json; b = [b for b in json.load(open('$BROWSERS'))['browsers'] if b['name'] == 'chromium-headless-shell'][0]"; \
    REVISION=$(python3 -c "$JSONQ; print(b['revision'])"); \
    VERSION=$(python3 -c "$JSONQ; print(b['browserVersion'])"); \
    DEST=/root/.cache/ms-playwright/chromium_headless_shell-$REVISION; \
    mkdir -p $DEST; \
    curl -fsSL -o /tmp/headless-shell.zip \
        "https://cdn.playwright.dev/builds/cft/$VERSION/linux64/chrome-headless-shell-linux64.zip"; \
    unzip -q /tmp/headless-shell.zip -d $DEST; \
    rm /tmp/headless-shell.zip; \
    touch $DEST/INSTALLATION_COMPLETE

FROM scratch

# Create required directories.
COPY --from=debs /home/tmp /tmp

# Chrome binary
COPY --from=pyapps /root/.cache/ms-playwright /root/.cache/ms-playwright

# Chrome libraries
COPY --from=debs /lib/x86_64-linux-gnu/libdl.so.2 \
                 /lib/x86_64-linux-gnu/libpthread.so.0 \
                 /lib/x86_64-linux-gnu/libglib-2.0.so.0 \
                 /lib/x86_64-linux-gnu/libgobject-2.0.so.0 \
                 /lib/x86_64-linux-gnu/libnss3.so \
                 /lib/x86_64-linux-gnu/libnssutil3.so \
                 /lib/x86_64-linux-gnu/libsmime3.so \
                 /lib/x86_64-linux-gnu/libnspr4.so \
                 /lib/x86_64-linux-gnu/libdbus-1.so.3 \
                 /lib/x86_64-linux-gnu/libatk-1.0.so.0 \
                 /lib/x86_64-linux-gnu/libatk-bridge-2.0.so.0 \
                 /lib/x86_64-linux-gnu/libcups.so.2 \
                 /lib/x86_64-linux-gnu/libgio-2.0.so.0 \
                 /lib/x86_64-linux-gnu/libdrm.so.2 \
                 /lib/x86_64-linux-gnu/libexpat.so.1 \
                 /lib/x86_64-linux-gnu/libxcb.so.1 \
                 /lib/x86_64-linux-gnu/libxkbcommon.so.0 \
                 /lib/x86_64-linux-gnu/libatspi.so.0 \
                 /lib/x86_64-linux-gnu/libX11.so.6 \
                 /lib/x86_64-linux-gnu/libXcomposite.so.1 \
                 /lib/x86_64-linux-gnu/libXdamage.so.1 \
                 /lib/x86_64-linux-gnu/libXext.so.6 \
                 /lib/x86_64-linux-gnu/libXfixes.so.3 \
                 /lib/x86_64-linux-gnu/libXrandr.so.2 \
                 /lib/x86_64-linux-gnu/libgbm.so.1 \
                 /lib/x86_64-linux-gnu/libpango-1.0.so.0 \
                 /lib/x86_64-linux-gnu/libcairo.so.2 \
                 /lib/x86_64-linux-gnu/libasound.so.2 \
                 /lib/x86_64-linux-gnu/libm.so.6 \
                 /lib/x86_64-linux-gnu/libgcc_s.so.1 \
                 /lib/x86_64-linux-gnu/libc.so.6 \
                 /lib/x86_64-linux-gnu/libpcre2-8.so.0 \
                 /lib/x86_64-linux-gnu/libffi.so.8 \
                 /lib/x86_64-linux-gnu/libplc4.so \
                 /lib/x86_64-linux-gnu/libplds4.so \
                 /lib/x86_64-linux-gnu/libsystemd.so.0 \
                 /lib/x86_64-linux-gnu/libgssapi_krb5.so.2 \
                 /lib/x86_64-linux-gnu/libavahi-common.so.3 \
                 /lib/x86_64-linux-gnu/libavahi-client.so.3 \
                 /lib/x86_64-linux-gnu/libgnutls.so.30 \
                 /lib/x86_64-linux-gnu/libz.so.1 \
                 /lib/x86_64-linux-gnu/libgmodule-2.0.so.0 \
                 /lib/x86_64-linux-gnu/libmount.so.1 \
                 /lib/x86_64-linux-gnu/libselinux.so.1 \
                 /lib/x86_64-linux-gnu/libXau.so.6 \
                 /lib/x86_64-linux-gnu/libXdmcp.so.6 \
                 /lib/x86_64-linux-gnu/libXi.so.6 \
                 /lib/x86_64-linux-gnu/libXrender.so.1 \
                 /lib/x86_64-linux-gnu/libwayland-server.so.0 \
                 /lib/x86_64-linux-gnu/libfribidi.so.0 \
                 /lib/x86_64-linux-gnu/libthai.so.0 \
                 /lib/x86_64-linux-gnu/libharfbuzz.so.0 \
                 /lib/x86_64-linux-gnu/libpixman-1.so.0 \
                 /lib/x86_64-linux-gnu/libfontconfig.so.1 \
                 /lib/x86_64-linux-gnu/libfreetype.so.6 \
                 /lib/x86_64-linux-gnu/libpng16.so.16 \
                 /lib/x86_64-linux-gnu/libxcb-shm.so.0 \
                 /lib/x86_64-linux-gnu/libxcb-render.so.0 \
                 /lib/x86_64-linux-gnu/libcap.so.2 \
                 /lib/x86_64-linux-gnu/libgcrypt.so.20 \
                 /lib/x86_64-linux-gnu/liblzma.so.5 \
                 /lib/x86_64-linux-gnu/libzstd.so.1 \
                 /lib/x86_64-linux-gnu/liblz4.so.1 \
                 /lib/x86_64-linux-gnu/libkrb5.so.3 \
                 /lib/x86_64-linux-gnu/libk5crypto.so.3 \
                 /lib/x86_64-linux-gnu/libcom_err.so.2 \
                 /lib/x86_64-linux-gnu/libkrb5support.so.0 \
                 /lib/x86_64-linux-gnu/libp11-kit.so.0 \
                 /lib/x86_64-linux-gnu/libidn2.so.0 \
                 /lib/x86_64-linux-gnu/libunistring.so.2 \
                 /lib/x86_64-linux-gnu/libtasn1.so.6 \
                 /lib/x86_64-linux-gnu/libnettle.so.8 \
                 /lib/x86_64-linux-gnu/libhogweed.so.6 \
                 /lib/x86_64-linux-gnu/libgmp.so.10 \
                 /lib/x86_64-linux-gnu/libblkid.so.1 \
                 /lib/x86_64-linux-gnu/libbsd.so.0 \
                 /lib/x86_64-linux-gnu/libdatrie.so.1 \
                 /lib/x86_64-linux-gnu/libgraphite2.so.3 \
                 /lib/x86_64-linux-gnu/libbrotlidec.so.1 \
                 /lib/x86_64-linux-gnu/libgpg-error.so.0 \
                 /lib/x86_64-linux-gnu/libkeyutils.so.1 \
                 /lib/x86_64-linux-gnu/libresolv.so.2 \
                 /lib/x86_64-linux-gnu/libmd.so.0 \
                 /lib/x86_64-linux-gnu/libbrotlicommon.so.1 \
                 /lib/x86_64-linux-gnu/

# Other Chrome-related libraries
COPY --from=debs /usr/lib/x86_64-linux-gnu/libsoftokn3.so \
                 /usr/lib/x86_64-linux-gnu/libsqlite3.so.0 \
                 /usr/lib/x86_64-linux-gnu/libudev.so.1 \
                 /usr/lib/x86_64-linux-gnu/libfreebl3.so \
                 /usr/lib/x86_64-linux-gnu/libfreeblpriv3.so \
                 /usr/lib/x86_64-linux-gnu/

# Python binary
COPY --from=debs /usr/bin/python3 /usr/bin/python3
COPY --from=debs /usr/bin/python /usr/bin/python

# Python libraries
COPY --from=debs /lib/x86_64-linux-gnu/libm.so.6 \
                 /lib/x86_64-linux-gnu/libz.so.1 \
                 /lib/x86_64-linux-gnu/libexpat.so.1 \
                 /lib/x86_64-linux-gnu/libc.so.6 \
                 /lib/x86_64-linux-gnu/

COPY --from=debs /usr/lib/python3.11 /usr/lib/python3.11

# Python packages and their CLI entry points
COPY --from=pyapps /x86-dist-packages /usr/lib/python3/dist-packages
COPY --from=pyapps /x86-bin /usr/bin

# System libraries
COPY --from=debs /lib/x86_64-linux-gnu/libc.so.6 \
                 /lib/x86_64-linux-gnu/libz.so.1 \
                 /lib/x86_64-linux-gnu/libbrotlidec.so.1 \
                 /lib/x86_64-linux-gnu/libbrotlienc.so.1 \
                 /lib/x86_64-linux-gnu/libcrypto.so.3 \
                 /lib/x86_64-linux-gnu/libssl.so.3 \
                 /lib/x86_64-linux-gnu/libstdc++.so.6 \
                 /lib/x86_64-linux-gnu/libm.so.6 \
                 /lib/x86_64-linux-gnu/libgcc_s.so.1 \
                 /lib/x86_64-linux-gnu/libpthread.so.0 \
                 /lib/x86_64-linux-gnu/libdl.so.2 \
                 /lib/x86_64-linux-gnu/libbrotlicommon.so.1 \
                 /lib/x86_64-linux-gnu/librt.so.1 \
                 /lib/x86_64-linux-gnu/libtinfo.so.6 \
                 /lib/x86_64-linux-gnu/libproc2.so.0 \
                 /lib/x86_64-linux-gnu/

COPY --from=debs /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=debs /etc/ld.so.cache /etc/ld.so.cache

# Data files
COPY --from=debs /usr/share/fonts /usr/share/fonts

COPY --from=debs /run /run

# Distro definition
COPY --from=debs /etc/os-release /etc/os-release
COPY --from=debs /usr/lib/os-release /usr/lib/os-release

# Configuration files
COPY --from=debs /etc /etc

# Required by wrapper script
COPY --from=debs /dash-amd64/bin/dash /bin/sh

# Required by Playwright / Chrome
COPY --from=debs /usr/bin/ps /usr/bin/ps

# Actual server implementation
COPY ./main.py /app/main.py

# Wrapper script set environment
COPY ./wrapper.sh /usr/bin/wrapper.sh
