FROM --platform=$BUILDPLATFORM alpine:3.20 AS base

###
### Build Postgres
###
FROM --platform=$BUILDPLATFORM base AS pg-build

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

# Build pg_ukc_scaletozero plugin
ADD https://github.com/unikraft-cloud/pg_ukc_scaletozero/archive/refs/heads/stable.zip /tmp/pg_ukc_scaletozero.zip

RUN mkdir /usr/src/pg_ukc_scaletozero; \
    unzip /tmp/pg_ukc_scaletozero.zip -d /tmp/extract; \
    mv /tmp/extract/pg_ukc_scaletozero-*/* /usr/src/pg_ukc_scaletozero

RUN cd /usr/src/pg_ukc_scaletozero; \
    export CFLAGS="-s -Os -Wl,--strip-all"; \
    make; \
    make install DESTDIR=/usr/src/postgresql/dist

##
## Retrieve dependencies
##
FROM --platform=$BUILDPLATFORM base AS base-deps

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
        openssl \
        krb5-libs \
        libldap \
        cyrus-sasl \
        libcom_err \
        keyutils-libs \
    ;

##
## Build root file system
##
FROM --platform=$BUILDPLATFORM busybox

# Libraries
COPY --from=base-deps /lib/ld-musl-x86_64.so.1 /lib/
COPY --from=base-deps /lib/libz.so.1 /lib/
COPY --from=base-deps /lib/libuuid.so.1 /lib/
COPY --from=base-deps /usr/lib/libgcc_s.so.1 /usr/lib/
COPY --from=base-deps /usr/lib/libstdc++.so.6 /usr/lib/
COPY --from=base-deps /usr/lib/liblz4.so.1 /usr/lib/
COPY --from=base-deps /usr/lib/liblzma.so.5 /usr/lib/
COPY --from=base-deps /usr/lib/libxml2.so.2 /usr/lib/
COPY --from=base-deps /usr/lib/libxslt.so.1 /usr/lib/
COPY --from=base-deps /usr/lib/libncursesw.so.6 /usr/lib/
COPY --from=base-deps /usr/lib/libreadline.so.8 /usr/lib/
COPY --from=base-deps /usr/lib/libedit.so.0 /usr/lib/
COPY --from=base-deps /lib/libssl.so.3 /lib/
COPY --from=base-deps /lib/libcrypto.so.3 /lib/
COPY --from=base-deps /usr/lib/libgssapi_krb5.so.2 /usr/lib/
COPY --from=base-deps /usr/lib/libkrb5.so.3 /usr/lib/
COPY --from=base-deps /usr/lib/libk5crypto.so.3 /usr/lib/
COPY --from=base-deps /usr/lib/libkrb5support.so.0 /usr/lib/
COPY --from=base-deps /usr/lib/libldap.so.2 /usr/lib/
COPY --from=base-deps /usr/lib/liblber.so.2 /usr/lib/
COPY --from=base-deps /usr/lib/libsasl2.so.3 /usr/lib/
COPY --from=base-deps /lib/libcom_err.so.2 /lib/
COPY --from=base-deps /usr/lib/libkeyutils.so.1 /usr/lib/
COPY --from=base-deps /usr/lib/libicudata.so.74 /usr/lib/
COPY --from=base-deps /usr/lib/libicuuc.so.74 /usr/lib/
COPY --from=base-deps /usr/lib/libicui18n.so.74 /usr/lib/

# Data files
COPY --from=base-deps /usr/share/icu /usr/share/icu
COPY --from=base-deps /usr/share/zoneinfo /usr/share/zoneinfo

# Bash
COPY --from=base-deps /bin/bash /bin/bash

# PostgreSQL binaries
COPY --from=pg-build /usr/src/postgresql/dist/ /

# Configuration and runtime files
COPY fs/ /

# Wrapper script
COPY --chmod=755 wrapper.sh /usr/local/bin/wrapper.sh
