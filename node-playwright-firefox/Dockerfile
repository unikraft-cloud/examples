FROM --platform=linux/x86_64 debian:bookworm AS build

ARG NODE_VERSION=22.8.0

RUN set -xe; \
    apt-get -yqq update; \
    apt-get -yqq install \
        build-essential \
        ca-certificates \
        curl \
        libasound2 \
        libatk1.0-0 \
        libatk-bridge2.0-0 \
        libatspi2.0-0 \
        libgbm1 \
        libgtk-3-0 \
        libnspr4 \
        libnss3 \
        libpango1.0-0 \
        libssl-dev \
        libx11-xcb1 \
        libxcomposite1 \
        libxfixes3 \
        libxkbcommon0 \
    ;

RUN set -xe; \
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash; \
    . ~/.bashrc; \
    nvm install ${NODE_VERSION} \
    ;

WORKDIR /app
COPY package* .

RUN set -xe; \
    . ~/.bashrc; \
    npm install \
    ;

# Node binary
RUN set -xe; \
    cp /root/.nvm/versions/node/v${NODE_VERSION}/bin/node /usr/bin/node \
    ;

RUN mkdir /home/tmp

FROM scratch

ARG NODE_VERSION=22.8.0

# Create required directories.
COPY --from=build /home/tmp /tmp

# Browser binary
COPY --from=build /root/.cache/ms-playwright /root/.cache/ms-playwright

# Browser libraries
COPY --from=build \
                  /lib/x86_64-linux-gnu/libasound.so.2 \
                  /lib/x86_64-linux-gnu/libatk-1.0.so.0 \
                  /lib/x86_64-linux-gnu/libatk-bridge-2.0.so.0 \
                  /lib/x86_64-linux-gnu/libatspi.so.0 \
                  /lib/x86_64-linux-gnu/libblkid.so.1 \
                  /lib/x86_64-linux-gnu/libbrotlicommon.so.1 \
                  /lib/x86_64-linux-gnu/libbrotlidec.so.1 \
                  /lib/x86_64-linux-gnu/libbsd.so.0 \
                  /lib/x86_64-linux-gnu/libcairo-gobject.so.2 \
                  /lib/x86_64-linux-gnu/libcairo.so.2 \
                  /lib/x86_64-linux-gnu/libcap.so.2 \
                  /lib/x86_64-linux-gnu/libc.so.6 \
                  /lib/x86_64-linux-gnu/libdatrie.so.1 \
                  /lib/x86_64-linux-gnu/libdbus-1.so.3 \
                  /lib/x86_64-linux-gnu/libdl.so.2 \
                  /lib/x86_64-linux-gnu/libepoxy.so.0 \
                  /lib/x86_64-linux-gnu/libexpat.so.1 \
                  /lib/x86_64-linux-gnu/libffi.so.8 \
                  /lib/x86_64-linux-gnu/libfontconfig.so.1 \
                  /lib/x86_64-linux-gnu/libfreetype.so.6 \
                  /lib/x86_64-linux-gnu/libfribidi.so.0 \
                  /lib/x86_64-linux-gnu/libgcc_s.so.1 \
                  /lib/x86_64-linux-gnu/libgcrypt.so.20 \
                  /lib/x86_64-linux-gnu/libgdk-3.so.0 \
                  /lib/x86_64-linux-gnu/libgdk_pixbuf-2.0.so.0 \
                  /lib/x86_64-linux-gnu/libgio-2.0.so.0 \
                  /lib/x86_64-linux-gnu/libglib-2.0.so.0 \
                  /lib/x86_64-linux-gnu/libgmodule-2.0.so.0 \
                  /lib/x86_64-linux-gnu/libgobject-2.0.so.0 \
                  /lib/x86_64-linux-gnu/libgpg-error.so.0 \
                  /lib/x86_64-linux-gnu/libgraphite2.so.3 \
                  /lib/x86_64-linux-gnu/libgtk-3.so.0 \
                  /lib/x86_64-linux-gnu/libharfbuzz.so.0 \
                  /lib/x86_64-linux-gnu/libjpeg.so.62 \
                  /lib/x86_64-linux-gnu/liblz4.so.1 \
                  /lib/x86_64-linux-gnu/liblzma.so.5 \
                  /lib/x86_64-linux-gnu/libmd.so.0 \
                  /lib/x86_64-linux-gnu/libmount.so.1 \
                  /lib/x86_64-linux-gnu/libm.so.6 \
                  /lib/x86_64-linux-gnu/libnspr4.so \
                  /lib/x86_64-linux-gnu/libnss3.so \
                  /lib/x86_64-linux-gnu/libnssutil3.so \
                  /lib/x86_64-linux-gnu/libpango-1.0.so.0 \
                  /lib/x86_64-linux-gnu/libpangocairo-1.0.so.0 \
                  /lib/x86_64-linux-gnu/libpangoft2-1.0.so.0 \
                  /lib/x86_64-linux-gnu/libpcre2-8.so.0 \
                  /lib/x86_64-linux-gnu/libpixman-1.so.0 \
                  /lib/x86_64-linux-gnu/libplc4.so \
                  /lib/x86_64-linux-gnu/libplds4.so \
                  /lib/x86_64-linux-gnu/libpng16.so.16 \
                  /lib/x86_64-linux-gnu/libpthread.so.0 \
                  /lib/x86_64-linux-gnu/libresolv.so.2 \
                  /lib/x86_64-linux-gnu/librt.so.1 \
                  /lib/x86_64-linux-gnu/libselinux.so.1 \
                  /lib/x86_64-linux-gnu/libsmime3.so \
                  /lib/x86_64-linux-gnu/libssl3.so \
                  /lib/x86_64-linux-gnu/libstdc++.so.6 \
                  /lib/x86_64-linux-gnu/libsystemd.so.0 \
                  /lib/x86_64-linux-gnu/libthai.so.0 \
                  /lib/x86_64-linux-gnu/libwayland-client.so.0 \
                  /lib/x86_64-linux-gnu/libwayland-cursor.so.0 \
                  /lib/x86_64-linux-gnu/libwayland-egl.so.1 \
                  /lib/x86_64-linux-gnu/libX11.so.6 \
                  /lib/x86_64-linux-gnu/libX11-xcb.so.1 \
                  /lib/x86_64-linux-gnu/libXau.so.6 \
                  /lib/x86_64-linux-gnu/libxcb-render.so.0 \
                  /lib/x86_64-linux-gnu/libxcb-shm.so.0 \
                  /lib/x86_64-linux-gnu/libxcb.so.1 \
                  /lib/x86_64-linux-gnu/libXcomposite.so.1 \
                  /lib/x86_64-linux-gnu/libXcursor.so.1 \
                  /lib/x86_64-linux-gnu/libXdamage.so.1 \
                  /lib/x86_64-linux-gnu/libXdmcp.so.6 \
                  /lib/x86_64-linux-gnu/libXext.so.6 \
                  /lib/x86_64-linux-gnu/libXfixes.so.3 \
                  /lib/x86_64-linux-gnu/libXinerama.so.1 \
                  /lib/x86_64-linux-gnu/libXi.so.6 \
                  /lib/x86_64-linux-gnu/libxkbcommon.so.0 \
                  /lib/x86_64-linux-gnu/libXrandr.so.2 \
                  /lib/x86_64-linux-gnu/libXrender.so.1 \
                  /lib/x86_64-linux-gnu/libz.so.1 \
                  /lib/x86_64-linux-gnu/libzstd.so.1 \
                  /lib/x86_64-linux-gnu/

# Node binary
COPY --from=build /root/.nvm/versions/node/v${NODE_VERSION}/bin/node /usr/bin/node

# Node libraries
COPY --from=build \
                  /lib/x86_64-linux-gnu/libc.so.6 \
                  /lib/x86_64-linux-gnu/libdl.so.2 \
                  /lib/x86_64-linux-gnu/libgcc_s.so.1 \
                  /lib/x86_64-linux-gnu/libm.so.6 \
                  /lib/x86_64-linux-gnu/libpthread.so.0 \
                  /lib/x86_64-linux-gnu/libstdc++.so.6 \
                  /lib/x86_64-linux-gnu/

# Loader / Dynamic linker
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=build /etc/ld.so.cache /etc/ld.so.cache

# Dbus and system files
COPY --from=build /usr/lib/dbus-1.0 /usr/lib/dbus-1.0
COPY --from=build /usr/lib/systemd /usr/lib/systemd
COPY --from=build /usr/lib/tmpfiles.d /usr/lib/tmpfiles.d
COPY --from=build /usr/lib/sysusers.d /usr/lib/sysusers.d
COPY --from=build /usr/lib/sysctl.d /usr/lib/sysctl.d

# Data files
COPY --from=build /usr/share/fonts /usr/share/fonts

# Run directory
COPY --from=build /run /run

# Distro definition
COPY --from=build /etc/os-release /etc/os-release
COPY --from=build /usr/lib/os-release /usr/lib/os-release

# Configuration files
COPY --from=build /etc /etc

# Node modules, including Puppeteer and application
COPY --from=build /app /app

# Required by wrapper script
COPY --from=build /bin/sh /bin/sh
COPY --from=build /usr/bin/chown /usr/bin/chown

# Actual server implementation
COPY ./server.js /app/server.js

# Wrapper script
COPY ./wrapper.sh /usr/bin/wrapper.sh

