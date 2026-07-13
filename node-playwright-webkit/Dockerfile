FROM --platform=linux/x86_64 debian:bookworm AS build

ARG NODE_VERSION=22.8.0

RUN set -xe; \
    apt-get -yqq update; \
    apt-get -yqq install \
        libatk1.0 \
        libatk-bridge2.0 \
        libatomic1 \
        libcairo-gobject2 \
        libenchant-2.2 \
        libepoxy0 \
        libevent-2.1 \
        libflite1 \
        libgdk-pixbuf-2.0 \
        libgles2 \
        libgstreamer1.0-0 \
        libgstreamer1.0-dev \
        libgstreamer-gl1.0-0 \
        libgstreamer-plugins-bad1.0-0 \
        libgstreamer-plugins-base1.0-0 \
        libgtk-3-0 \
        libharfbuzz-icu0 \
        libhyphen0 \
        liblcms2-2 \
        libmanette-0.2-0 \
        libopus0 \
        libpango-1.0 \
        libpangocairo-1.0 \
        libsecret-1-0 \
        libtinfo6 \
        libvpx7 \
        libwebpdemux2 \
        libwebpmux3 \
        libwoff1 \
        libx264-164 \
        libx264-dev \
        libxslt1.1 \
    ; \
    apt-get -yqq install \
        ca-certificates \
        curl \
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
                  /usr/lib/x86_64-linux-gnu/libabsl_base.so.20220623 \
                  /usr/lib/x86_64-linux-gnu/libabsl_debugging_internal.so.20220623 \
                  /usr/lib/x86_64-linux-gnu/libabsl_demangle_internal.so.20220623 \
                  /usr/lib/x86_64-linux-gnu/libabsl_graphcycles_internal.so.20220623 \
                  /usr/lib/x86_64-linux-gnu/libabsl_int128.so.20220623 \
                  /usr/lib/x86_64-linux-gnu/libabsl_malloc_internal.so.20220623 \
                  /usr/lib/x86_64-linux-gnu/libabsl_raw_logging_internal.so.20220623 \
                  /usr/lib/x86_64-linux-gnu/libabsl_spinlock_wait.so.20220623 \
                  /usr/lib/x86_64-linux-gnu/libabsl_stacktrace.so.20220623 \
                  /usr/lib/x86_64-linux-gnu/libabsl_strings_internal.so.20220623 \
                  /usr/lib/x86_64-linux-gnu/libabsl_strings.so.20220623 \
                  /usr/lib/x86_64-linux-gnu/libabsl_symbolize.so.20220623 \
                  /usr/lib/x86_64-linux-gnu/libabsl_synchronization.so.20220623 \
                  /usr/lib/x86_64-linux-gnu/libabsl_throw_delegate.so.20220623 \
                  /usr/lib/x86_64-linux-gnu/libabsl_time.so.20220623 \
                  /usr/lib/x86_64-linux-gnu/libabsl_time_zone.so.20220623 \
                  /usr/lib/x86_64-linux-gnu/libaom.so.3 \
                  /usr/lib/x86_64-linux-gnu/libasound.so.2 \
                  /usr/lib/x86_64-linux-gnu/libatk-1.0.so.0 \
                  /usr/lib/x86_64-linux-gnu/libatk-bridge-2.0.so.0 \
                  /usr/lib/x86_64-linux-gnu/libatomic.so.1 \
                  /usr/lib/x86_64-linux-gnu/libatspi.so.0 \
                  /usr/lib/x86_64-linux-gnu/libavif.so.15 \
                  /usr/lib/x86_64-linux-gnu/libblkid.so.1 \
                  /usr/lib/x86_64-linux-gnu/libbrotlicommon.so.1 \
                  /usr/lib/x86_64-linux-gnu/libbrotlidec.so.1 \
                  /usr/lib/x86_64-linux-gnu/libbsd.so.0 \
                  /usr/lib/x86_64-linux-gnu/libbz2.so.1.0 \
                  /usr/lib/x86_64-linux-gnu/libcairo-gobject.so.2 \
                  /usr/lib/x86_64-linux-gnu/libcairo.so.2 \
                  /usr/lib/x86_64-linux-gnu/libcap.so.2 \
                  /usr/lib/x86_64-linux-gnu/libcom_err.so.2 \
                  /usr/lib/x86_64-linux-gnu/libc.so.6 \
                  /usr/lib/x86_64-linux-gnu/libdatrie.so.1 \
                  /usr/lib/x86_64-linux-gnu/libdav1d.so.6 \
                  /usr/lib/x86_64-linux-gnu/libdbus-1.so.3 \
                  /usr/lib/x86_64-linux-gnu/libdl.so.2 \
                  /usr/lib/x86_64-linux-gnu/libdrm_amdgpu.so.1 \
                  /usr/lib/x86_64-linux-gnu/libdrm_intel.so.1 \
                  /usr/lib/x86_64-linux-gnu/libdrm_nouveau.so.2 \
                  /usr/lib/x86_64-linux-gnu/libdrm_radeon.so.1 \
                  /usr/lib/x86_64-linux-gnu/libdrm.so.2 \
                  /usr/lib/x86_64-linux-gnu/libdw.so.1 \
                  /usr/lib/x86_64-linux-gnu/libedit.so.2 \
                  /usr/lib/x86_64-linux-gnu/libEGL_mesa.so.0 \
                  /usr/lib/x86_64-linux-gnu/libEGL.so.1 \
                  /usr/lib/x86_64-linux-gnu/libelf.so.1 \
                  /usr/lib/x86_64-linux-gnu/libenchant-2.so.2 \
                  /usr/lib/x86_64-linux-gnu/libepoxy.so.0 \
                  /usr/lib/x86_64-linux-gnu/libevdev.so.2 \
                  /usr/lib/x86_64-linux-gnu/libevent-2.1.so.7 \
                  /usr/lib/x86_64-linux-gnu/libexpat.so.1 \
                  /usr/lib/x86_64-linux-gnu/libffi.so.8 \
                  /usr/lib/x86_64-linux-gnu/libflite_cmu_grapheme_lang.so.1 \
                  /usr/lib/x86_64-linux-gnu/libflite_cmu_grapheme_lex.so.1 \
                  /usr/lib/x86_64-linux-gnu/libflite_cmu_indic_lang.so.1 \
                  /usr/lib/x86_64-linux-gnu/libflite_cmu_indic_lex.so.1 \
                  /usr/lib/x86_64-linux-gnu/libflite_cmulex.so.1 \
                  /usr/lib/x86_64-linux-gnu/libflite_cmu_time_awb.so.1 \
                  /usr/lib/x86_64-linux-gnu/libflite_cmu_us_awb.so.1 \
                  /usr/lib/x86_64-linux-gnu/libflite_cmu_us_kal16.so.1 \
                  /usr/lib/x86_64-linux-gnu/libflite_cmu_us_kal.so.1 \
                  /usr/lib/x86_64-linux-gnu/libflite_cmu_us_rms.so.1 \
                  /usr/lib/x86_64-linux-gnu/libflite_cmu_us_slt.so.1 \
                  /usr/lib/x86_64-linux-gnu/libflite.so.1 \
                  /usr/lib/x86_64-linux-gnu/libflite_usenglish.so.1 \
                  /usr/lib/x86_64-linux-gnu/libfontconfig.so.1 \
                  /usr/lib/x86_64-linux-gnu/libfreetype.so.6 \
                  /usr/lib/x86_64-linux-gnu/libfribidi.so.0 \
                  /usr/lib/x86_64-linux-gnu/libgav1.so.1 \
                  /usr/lib/x86_64-linux-gnu/libgbm.so.1 \
                  /usr/lib/x86_64-linux-gnu/libgcc_s.so.1 \
                  /usr/lib/x86_64-linux-gnu/libgcrypt.so.20 \
                  /usr/lib/x86_64-linux-gnu/libgdk-3.so.0 \
                  /usr/lib/x86_64-linux-gnu/libgdk_pixbuf-2.0.so.0 \
                  /usr/lib/x86_64-linux-gnu/libgio-2.0.so.0 \
                  /usr/lib/x86_64-linux-gnu/libglapi.so.0 \
                  /usr/lib/x86_64-linux-gnu/libGLdispatch.so.0 \
                  /usr/lib/x86_64-linux-gnu/libGLESv2.so.2 \
                  /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0 \
                  /usr/lib/x86_64-linux-gnu/libGL.so.1 \
                  /usr/lib/x86_64-linux-gnu/libGLX.so.0 \
                  /usr/lib/x86_64-linux-gnu/libgmodule-2.0.so.0 \
                  /usr/lib/x86_64-linux-gnu/libgmp.so.10 \
                  /usr/lib/x86_64-linux-gnu/libgnutls.so.30 \
                  /usr/lib/x86_64-linux-gnu/libgobject-2.0.so.0 \
                  /usr/lib/x86_64-linux-gnu/libgpg-error.so.0 \
                  /usr/lib/x86_64-linux-gnu/libgraphite2.so.3 \
                  /usr/lib/x86_64-linux-gnu/libgssapi_krb5.so.2 \
                  /usr/lib/x86_64-linux-gnu/libgstallocators-1.0.so.0 \
                  /usr/lib/x86_64-linux-gnu/libgstapp-1.0.so.0 \
                  /usr/lib/x86_64-linux-gnu/libgstaudio-1.0.so.0 \
                  /usr/lib/x86_64-linux-gnu/libgstbase-1.0.so.0 \
                  /usr/lib/x86_64-linux-gnu/libgstcodecparsers-1.0.so.0 \
                  /usr/lib/x86_64-linux-gnu/libgstfft-1.0.so.0 \
                  /usr/lib/x86_64-linux-gnu/libgstgl-1.0.so.0 \
                  /usr/lib/x86_64-linux-gnu/libgstpbutils-1.0.so.0 \
                  /usr/lib/x86_64-linux-gnu/libgstreamer-1.0.so.0 \
                  /usr/lib/x86_64-linux-gnu/libgsttag-1.0.so.0 \
                  /usr/lib/x86_64-linux-gnu/libgstvideo-1.0.so.0 \
                  /usr/lib/x86_64-linux-gnu/libgtk-3.so.0 \
                  /usr/lib/x86_64-linux-gnu/libgudev-1.0.so.0 \
                  /usr/lib/x86_64-linux-gnu/libharfbuzz-icu.so.0 \
                  /usr/lib/x86_64-linux-gnu/libharfbuzz.so.0 \
                  /usr/lib/x86_64-linux-gnu/libhogweed.so.6 \
                  /usr/lib/x86_64-linux-gnu/libhyphen.so.0 \
                  /usr/lib/x86_64-linux-gnu/libicudata.so.72 \
                  /usr/lib/x86_64-linux-gnu/libicui18n.so.72 \
                  /usr/lib/x86_64-linux-gnu/libicuuc.so.72 \
                  /usr/lib/x86_64-linux-gnu/libidn2.so.0 \
                  /usr/lib/x86_64-linux-gnu/libjpeg.so.62 \
                  /usr/lib/x86_64-linux-gnu/libk5crypto.so.3 \
                  /usr/lib/x86_64-linux-gnu/libkeyutils.so.1 \
                  /usr/lib/x86_64-linux-gnu/libkrb5.so.3 \
                  /usr/lib/x86_64-linux-gnu/libkrb5support.so.0 \
                  /usr/lib/x86_64-linux-gnu/liblcms2.so.2 \
                  /usr/lib/x86_64-linux-gnu/libLLVM-15.so.1 \
                  /usr/lib/x86_64-linux-gnu/liblz4.so.1 \
                  /usr/lib/x86_64-linux-gnu/liblzma.so.5 \
                  /usr/lib/x86_64-linux-gnu/libmanette-0.2.so.0 \
                  /usr/lib/x86_64-linux-gnu/libmd.so.0 \
                  /usr/lib/x86_64-linux-gnu/libmount.so.1 \
                  /usr/lib/x86_64-linux-gnu/libm.so.6 \
                  /usr/lib/x86_64-linux-gnu/libnettle.so.8 \
                  /usr/lib/x86_64-linux-gnu/libnghttp2.so.14 \
                  /usr/lib/x86_64-linux-gnu/libopus.so.0 \
                  /usr/lib/x86_64-linux-gnu/liborc-0.4.so.0 \
                  /usr/lib/x86_64-linux-gnu/libp11-kit.so.0 \
                  /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0 \
                  /usr/lib/x86_64-linux-gnu/libpangocairo-1.0.so.0 \
                  /usr/lib/x86_64-linux-gnu/libpangoft2-1.0.so.0 \
                  /usr/lib/x86_64-linux-gnu/libpciaccess.so.0 \
                  /usr/lib/x86_64-linux-gnu/libpcre2-8.so.0 \
                  /usr/lib/x86_64-linux-gnu/libpixman-1.so.0 \
                  /usr/lib/x86_64-linux-gnu/libpng16.so.16 \
                  /usr/lib/x86_64-linux-gnu/libproxy.so.1 \
                  /usr/lib/x86_64-linux-gnu/libpsl.so.5 \
                  /usr/lib/x86_64-linux-gnu/libpthread.so.0 \
                  /usr/lib/x86_64-linux-gnu/librav1e.so.0 \
                  /usr/lib/x86_64-linux-gnu/libresolv.so.2 \
                  /usr/lib/x86_64-linux-gnu/libsecret-1.so.0 \
                  /usr/lib/x86_64-linux-gnu/libselinux.so.1 \
                  /usr/lib/x86_64-linux-gnu/libsensors.so.5 \
                  /usr/lib/x86_64-linux-gnu/libsoup-3.0.so.0 \
                  /usr/lib/x86_64-linux-gnu/libsqlite3.so.0 \
                  /usr/lib/x86_64-linux-gnu/libstdc++.so.6 \
                  /usr/lib/x86_64-linux-gnu/libSvtAv1Enc.so.1 \
                  /usr/lib/x86_64-linux-gnu/libsystemd.so.0 \
                  /usr/lib/x86_64-linux-gnu/libtasn1.so.6 \
                  /usr/lib/x86_64-linux-gnu/libthai.so.0 \
                  /usr/lib/x86_64-linux-gnu/libtinfo.so.6 \
                  /usr/lib/x86_64-linux-gnu/libudev.so.1 \
                  /usr/lib/x86_64-linux-gnu/libunistring.so.2 \
                  /usr/lib/x86_64-linux-gnu/libunwind.so.8 \
                  /usr/lib/x86_64-linux-gnu/libvpx.so.7 \
                  /usr/lib/x86_64-linux-gnu/libwayland-client.so.0 \
                  /usr/lib/x86_64-linux-gnu/libwayland-cursor.so.0 \
                  /usr/lib/x86_64-linux-gnu/libwayland-egl.so.1 \
                  /usr/lib/x86_64-linux-gnu/libwayland-server.so.0 \
                  /usr/lib/x86_64-linux-gnu/libwebpdemux.so.2 \
                  /usr/lib/x86_64-linux-gnu/libwebpmux.so.3 \
                  /usr/lib/x86_64-linux-gnu/libwebp.so.7 \
                  /usr/lib/x86_64-linux-gnu/libwoff2common.so.1.0.2 \
                  /usr/lib/x86_64-linux-gnu/libwoff2dec.so.1.0.2 \
                  /usr/lib/x86_64-linux-gnu/libX11.so.6 \
                  /usr/lib/x86_64-linux-gnu/libX11-xcb.so.1 \
                  /usr/lib/x86_64-linux-gnu/libXau.so.6 \
                  /usr/lib/x86_64-linux-gnu/libxcb-dri2.so.0 \
                  /usr/lib/x86_64-linux-gnu/libxcb-dri3.so.0 \
                  /usr/lib/x86_64-linux-gnu/libxcb-present.so.0 \
                  /usr/lib/x86_64-linux-gnu/libxcb-randr.so.0 \
                  /usr/lib/x86_64-linux-gnu/libxcb-render.so.0 \
                  /usr/lib/x86_64-linux-gnu/libxcb-shm.so.0 \
                  /usr/lib/x86_64-linux-gnu/libxcb.so.1 \
                  /usr/lib/x86_64-linux-gnu/libxcb-sync.so.1 \
                  /usr/lib/x86_64-linux-gnu/libxcb-xfixes.so.0 \
                  /usr/lib/x86_64-linux-gnu/libXcomposite.so.1 \
                  /usr/lib/x86_64-linux-gnu/libXcursor.so.1 \
                  /usr/lib/x86_64-linux-gnu/libXdamage.so.1 \
                  /usr/lib/x86_64-linux-gnu/libXdmcp.so.6 \
                  /usr/lib/x86_64-linux-gnu/libXext.so.6 \
                  /usr/lib/x86_64-linux-gnu/libXfixes.so.3 \
                  /usr/lib/x86_64-linux-gnu/libXinerama.so.1 \
                  /usr/lib/x86_64-linux-gnu/libXi.so.6 \
                  /usr/lib/x86_64-linux-gnu/libxkbcommon.so.0 \
                  /usr/lib/x86_64-linux-gnu/libxml2.so.2 \
                  /usr/lib/x86_64-linux-gnu/libXrandr.so.2 \
                  /usr/lib/x86_64-linux-gnu/libXrender.so.1 \
                  /usr/lib/x86_64-linux-gnu/libxshmfence.so.1 \
                  /usr/lib/x86_64-linux-gnu/libxslt.so.1 \
                  /usr/lib/x86_64-linux-gnu/libyuv.so.0 \
                  /usr/lib/x86_64-linux-gnu/libz3.so.4 \
                  /usr/lib/x86_64-linux-gnu/libz.so.1 \
                  /usr/lib/x86_64-linux-gnu/libzstd.so.1 \
                  /usr/lib/x86_64-linux-gnu/

COPY --from=build \
                  /usr/lib/x86_64-linux-gnu/dri \
                  /usr/lib/x86_64-linux-gnu/dri

COPY --from=build \
                  /usr/lib/x86_64-linux-gnu/gstreamer-1.0 \
                  /usr/lib/x86_64-linux-gnu/gstreamer-1.0

COPY --from=build \
                  /usr/lib/x86_64-linux-gnu/gconv \
                  /usr/lib/x86_64-linux-gnu/gconv

COPY --from=build \
                  /usr/lib/x86_64-linux-gnu/gio \
                  /usr/lib/x86_64-linux-gnu/gio

COPY --from=build \
                  /usr/lib/locale \
                  /usr/lib/locale

COPY --from=build \
                  /usr/lib/x86_64-linux-gnu/dri \
                  /usr/lib/dri

# Node binary
COPY --from=build /root/.nvm/versions/node/v${NODE_VERSION}/bin/node /usr/bin/node

# Node libraries
COPY --from=build \
                  /usr/lib/x86_64-linux-gnu/libc.so.6 \
                  /usr/lib/x86_64-linux-gnu/libdl.so.2 \
                  /usr/lib/x86_64-linux-gnu/libgcc_s.so.1 \
                  /usr/lib/x86_64-linux-gnu/libm.so.6 \
                  /usr/lib/x86_64-linux-gnu/libpthread.so.0 \
                  /usr/lib/x86_64-linux-gnu/libstdc++.so.6 \
                  /usr/lib/x86_64-linux-gnu/

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
COPY --from=build /usr/share/glib-2.0 /usr/share/glib-2.0
COPY --from=build /usr/share/glvnd /usr/share/glvnd

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

# Actual server implementation
COPY ./server.js /app/server.js

# Required by helper script pw_run.sh
COPY --from=build /bin/bash /bin/bash
COPY --from=build /usr/bin/env /usr/bin/env
COPY --from=build /usr/bin/uname /usr/bin/uname
COPY --from=build /usr/bin/dirname /usr/bin/dirname
COPY --from=build /usr/bin/readlink /usr/bin/readlink
COPY --from=build /usr/bin/ln /usr/bin/ln

# Libraries for helper utilities
COPY --from=build \
                  /usr/lib/x86_64-linux-gnu/libc.so.6 \
                  /usr/lib/x86_64-linux-gnu/libtinfo.so.6 \
                  /usr/lib/x86_64-linux-gnu/

# Create symlinks for library directories.
RUN /usr/bin/ln -sfn /usr/lib /lib

# Wrapper script
COPY ./wrapper.sh /usr/bin/wrapper.sh
