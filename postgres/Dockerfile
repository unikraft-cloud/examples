FROM alpine:3.20 AS base

FROM base AS pg-build

ENV PG_VERSION=16.4

RUN apk add --no-cache --virtual .build-deps \
        coreutils \
        g++ \
        gcc \
        make \
        tar \
        bzip2 \
        libxml2-dev \
        libxslt-dev \
        libedit-dev \
        zlib-dev \
        lz4-dev \
        zstd-dev \
        e2fsprogs-dev \
        linux-headers \
        unzip \
        git \
        icu-dev \
    ; \
    mkdir -p /usr/src; \
    mv /lib/libssl.so.3 /lib/libssl.so.3.orig

ADD https://ftp.postgresql.org/pub/source/v$PG_VERSION/postgresql-$PG_VERSION.tar.bz2 /tmp/postgresql-$PG_VERSION.tar.bz2

RUN tar -xvjf /tmp/postgresql-$PG_VERSION.tar.bz2 -C /usr/src
ADD allow-root.patch /usr/src/postgresql-$PG_VERSION/

RUN set -e; \
    cd /usr/src/postgresql-$PG_VERSION; \
    git apply allow-root.patch; \
    export CFLAGS="-s -Os -Wl,--strip-all"; \
    export CXXFLAGS="-s -Os -Wl,--strip-all"; \
    ./configure \
        --enable-option-checking=fatal \
        --enable-integer-datetimes \
        --enable-thread-safety \
        --disable-rpath \
        --with-uuid=e2fs \
        --with-pgport=5432 \
        --with-system-tzdata=/usr/share/zoneinfo \
        --prefix=/usr/local \
        --with-includes=/usr/local/include \
        --with-libraries=/usr/local/lib \
        --with-icu \
        --with-libxml \
        --with-libxslt \
        --without-zlib \
        --with-lz4 \
    ; \
    make -j "$(nproc)" world-bin; \
    make install-world-bin DESTDIR=/usr/src/postgresql/dist; \
    make install

ADD https://github.com/unikraft-cloud/pg_ukc_scaletozero/archive/refs/heads/stable.zip /tmp/pg_ukc_scaletozero.zip

RUN mkdir /usr/src/pg_ukc_scaletozero; \
    unzip /tmp/pg_ukc_scaletozero.zip -d /tmp/extract; \
    mv /tmp/extract/pg_ukc_scaletozero-*/* /usr/src/pg_ukc_scaletozero

RUN cd /usr/src/pg_ukc_scaletozero; \
    export CFLAGS="-s -Os -Wl,--strip-all"; \
    make; \
    make install DESTDIR=/usr/src/postgresql/dist

FROM base AS build

RUN apk add --no-cache \
        libuuid \
        libxml2 \
        libxslt \
        lz4-libs \
        tzdata \
        libgcc \
        libstdc++ \
        icu-libs \
        bash \
        libedit \
        lddtree \
        pax-utils \
    ;

COPY --from=pg-build /usr/src/postgresql/dist/ /

RUN set -xe; \
    mkdir -p /rootfs/dev /rootfs/sbin /rootfs/usr/bin /rootfs/usr/sbin; \
    find /bin/busybox /bin/bash /usr/local -type f -exec scanelf -BF '%F' {} + | tr '\n' '\0' | xargs -0 -r lddtree -l | sort -u > /tmp/libs.txt; \
    tar -cf /tmp/libs.tar -T /tmp/libs.txt; \
    tar -C /rootfs -xf /tmp/libs.tar; \
    tar -C / -cf /tmp/data.tar etc/group usr/local/lib usr/local/share usr/share/icu usr/share/zoneinfo; \
    tar -C /rootfs -xf /tmp/data.tar; \
    chroot /rootfs /bin/busybox --install -s

COPY fs/ /rootfs/
COPY --chmod=755 wrapper.sh /rootfs/usr/local/bin/wrapper.sh

RUN set -xe; \
    chmod 1777 /rootfs/tmp; \
    mknod -m 666 /rootfs/dev/null c 1 3; \
    mknod -m 444 /rootfs/dev/urandom c 1 9; \
    chroot /rootfs /usr/local/bin/postgres --version; \
    chroot /rootfs /usr/local/bin/initdb -D /tmp/pgdata; \
    echo 'SELECT 1;' | chroot /rootfs /usr/local/bin/postgres --single -D /tmp/pgdata -c shared_preload_libraries=pg_ukc_scaletozero postgres; \
    chroot /rootfs /usr/bin/env bash -c 'mkdir -p /tmp/x && chmod 700 /tmp/x && ls /tmp/x && cat /etc/passwd'; \
    rm -rf /rootfs/dev/null /rootfs/dev/urandom /rootfs/tmp/pgdata /rootfs/tmp/x

FROM scratch

COPY --from=build /rootfs /
