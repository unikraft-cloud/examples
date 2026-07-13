# Postgres must be compiled from source (allow-root.patch rules out prebuilt
# binaries), but no build step needs to *execute* x86_64 code, so every stage
# runs natively on the build host: the compiler is Debian's packaged amd64
# cross toolchain (on x86_64 hosts the same `x86_64-linux-gnu-gcc` name is
# provided by native gcc), and the libraries Postgres builds against and
# ships with are prebuilt amd64 Debian packages unpacked by native dpkg via
# multiarch.

###
### Cross-build Postgres
###
FROM --platform=$BUILDPLATFORM debian:bookworm AS pg-build

ENV PG_VERSION=16.4

RUN set -xe; \
    dpkg --add-architecture amd64; \
    apt-get -yqq update; \
    apt-get -yqq install --no-install-recommends \
        # x86_64 cross toolchain; resolves to native gcc on x86_64 hosts
        crossbuild-essential-amd64 \
        libc6-dev:amd64 \
        # prebuilt x86_64 libraries Postgres links against
        libicu-dev:amd64 \
        libxml2-dev:amd64 \
        libxslt1-dev:amd64 \
        liblz4-dev:amd64 \
        uuid-dev:amd64 \
        libedit-dev:amd64 \
        # build tools, all run natively
        make \
        pkg-config \
        bison \
        flex \
        patch \
        bzip2 \
        unzip \
    ; \
    mkdir -p /usr/src

ADD https://ftp.postgresql.org/pub/source/v$PG_VERSION/postgresql-$PG_VERSION.tar.bz2 /tmp/postgresql-$PG_VERSION.tar.bz2

RUN tar -xjf /tmp/postgresql-$PG_VERSION.tar.bz2 -C /usr/src
ADD allow-root.patch /usr/src/postgresql-$PG_VERSION/

# --host makes this a cross build on ARM hosts; on x86_64 hosts it is the
# native triplet and configure behaves as before.  PKG_CONFIG_LIBDIR points
# pkg-config at the amd64 multiarch .pc files so ICU resolves for the
# target, not the build host.
RUN set -e; \
    cd /usr/src/postgresql-$PG_VERSION; \
    patch -p1 < allow-root.patch; \
    export CFLAGS="-s -Os -Wl,--strip-all"; \
    export PKG_CONFIG_LIBDIR=/usr/lib/x86_64-linux-gnu/pkgconfig:/usr/lib/pkgconfig:/usr/share/pkgconfig; \
    ./configure \
        --host=x86_64-linux-gnu \
        --enable-option-checking=fatal \
        --enable-integer-datetimes \
        --enable-thread-safety \
        --disable-rpath \
        --with-uuid=e2fs \
        --with-pgport=5432 \
        --with-system-tzdata=/usr/share/zoneinfo \
        --prefix=/usr/local \
        --with-icu \
        --with-libxml \
        --with-libxslt \
        --without-zlib \
        --with-lz4 \
    ; \
    make -j "$(nproc)" world-bin; \
    make install-world-bin DESTDIR=/usr/src/postgresql/dist

# Build pg_ukc_scaletozero plugin.  It is a single-file PGXS module (one
# shared object, no SQL scripts), compiled directly against the Postgres
# build tree because PGXS would invoke pg_config, an x86_64 binary.
ADD https://github.com/unikraft-cloud/pg_ukc_scaletozero/archive/refs/heads/stable.zip /tmp/pg_ukc_scaletozero.zip

RUN mkdir /usr/src/pg_ukc_scaletozero; \
    unzip /tmp/pg_ukc_scaletozero.zip -d /tmp/extract; \
    mv /tmp/extract/pg_ukc_scaletozero-*/* /usr/src/pg_ukc_scaletozero

RUN set -e; \
    cd /usr/src/pg_ukc_scaletozero; \
    x86_64-linux-gnu-gcc -s -Os -fPIC -shared \
        -I/usr/src/postgresql-$PG_VERSION/src/include \
        -o pg_ukc_scaletozero.so pg_ukc_scaletozero.c; \
    install -D -m 755 pg_ukc_scaletozero.so \
        /usr/src/postgresql/dist/usr/local/lib/postgresql/pg_ukc_scaletozero.so

##
## Retrieve dependencies as prebuilt x86_64 packages
##
FROM --platform=$BUILDPLATFORM debian:bookworm AS runtime-deps

# dpkg-deb -x unpacks the amd64 debs without running any of their
# (x86_64) maintainer scripts.
RUN set -xe; \
    dpkg --add-architecture amd64; \
    apt-get -yqq update; \
    apt-get -yqq install --no-install-recommends locales; \
    mkdir /debs; \
    cd /debs; \
    apt-get -yqq download \
        libc6:amd64 \
        libicu72:amd64 \
        libxml2:amd64 \
        libxslt1.1:amd64 \
        liblz4-1:amd64 \
        libuuid1:amd64 \
        libedit2:amd64 \
        libbsd0:amd64 \
        libmd0:amd64 \
        libtinfo6:amd64 \
        zlib1g:amd64 \
        liblzma5:amd64 \
        libstdc++6:amd64 \
        libgcc-s1:amd64 \
        bash:amd64 \
        tzdata; \
    for deb in *.deb; do dpkg-deb -x "$deb" /rootfs; done

# wrapper.sh runs initdb with LANG=en_US.utf8, which glibc only accepts if
# the compiled locale exists (musl faked it; glibc does not).  Compiled
# glibc locales are architecture-independent, so the native localedef
# output is valid for the x86_64 rootfs.
RUN set -xe; \
    localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8; \
    mkdir -p /rootfs/usr/lib/locale; \
    cp /usr/lib/locale/locale-archive /rootfs/usr/lib/locale/

##
## Build root file system
##
# busybox:musl is a statically linked musl build, so its applets (including
# the /usr/bin/env that runs wrapper.sh's shebang, plus mkdir/chmod/ls/cat)
# carry no glibc dependency.  The default busybox:latest is glibc and ships
# its own libc.so.6; the glibc COPYs below overwrite that path with bookworm's
# older libc (2.36), which would leave every busybox applet demanding a
# GLIBC_2.38 the bundled libc no longer provides.  Keeping busybox on musl
# lets it coexist with the glibc that Postgres and bash are bundled against.
FROM --platform=linux/x86_64 busybox:musl

# Dynamic loader at the ELF interpreter path.  /lib/x86_64-linux-gnu and
# /usr/lib/x86_64-linux-gnu are its compiled-in search paths, so no
# ld.so.cache is needed.  The deb's own /lib64 entry is an absolute symlink
# that dangles inside /rootfs, so copy the real file.
COPY --from=runtime-deps /rootfs/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2

# Libraries
COPY --from=runtime-deps /rootfs/lib/x86_64-linux-gnu/libc.so.6 \
                         /rootfs/lib/x86_64-linux-gnu/libm.so.6 \
                         /rootfs/lib/x86_64-linux-gnu/libgcc_s.so.1 \
                         /rootfs/lib/x86_64-linux-gnu/libz.so.1 \
                         /rootfs/lib/x86_64-linux-gnu/liblzma.so.5 \
                         /rootfs/lib/x86_64-linux-gnu/libtinfo.so.6 \
                         /lib/x86_64-linux-gnu/

COPY --from=runtime-deps /rootfs/usr/lib/x86_64-linux-gnu/libicudata.so.72 \
                         /rootfs/usr/lib/x86_64-linux-gnu/libicuuc.so.72 \
                         /rootfs/usr/lib/x86_64-linux-gnu/libicui18n.so.72 \
                         /rootfs/usr/lib/x86_64-linux-gnu/libstdc++.so.6 \
                         /rootfs/usr/lib/x86_64-linux-gnu/libxml2.so.2 \
                         /rootfs/usr/lib/x86_64-linux-gnu/libxslt.so.1 \
                         /rootfs/usr/lib/x86_64-linux-gnu/liblz4.so.1 \
                         /rootfs/usr/lib/x86_64-linux-gnu/libuuid.so.1 \
                         /rootfs/usr/lib/x86_64-linux-gnu/libedit.so.2 \
                         /rootfs/usr/lib/x86_64-linux-gnu/libbsd.so.0 \
                         /rootfs/usr/lib/x86_64-linux-gnu/libmd.so.0 \
                         /usr/lib/x86_64-linux-gnu/

# Data files
COPY --from=runtime-deps /rootfs/usr/share/zoneinfo /usr/share/zoneinfo
COPY --from=runtime-deps /rootfs/usr/lib/locale /usr/lib/locale

# Bash, for wrapper.sh
COPY --from=runtime-deps /rootfs/bin/bash /bin/bash

# PostgreSQL binaries
COPY --from=pg-build /usr/src/postgresql/dist/ /

# glibc's loader does not search /usr/local/lib (musl's did), so libpq must
# also live in a searched directory for psql and friends.
COPY --from=pg-build /usr/src/postgresql/dist/usr/local/lib/libpq.so.5 /usr/lib/x86_64-linux-gnu/

# Configuration and runtime files
COPY fs/ /

# Wrapper script
COPY --chmod=755 wrapper.sh /usr/local/bin/wrapper.sh
