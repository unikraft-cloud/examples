FROM postgres:16.2-alpine AS base

FROM base AS ext-build
RUN apk add --no-cache gcc make musl-dev llvm15-dev clang15 unzip
ADD https://github.com/kraftcloud/pg_ukc_scaletozero/archive/refs/heads/stable.zip /tmp/src.zip
RUN mkdir /src && \
    unzip /tmp/src.zip -d /tmp/extract && \
    mv /tmp/extract/pg_ukc_scaletozero-*/* /src
RUN cd /src && \
    make && \
    make install DESTDIR=/out

FROM base AS runtime

RUN apk add --no-cache lddtree pax-utils

COPY --from=ext-build /out/usr/local/lib/postgresql/pg_ukc_scaletozero.so /usr/local/lib/postgresql/pg_ukc_scaletozero.so

RUN set -xe; \
    mkdir -p /rootfs/dev; \
    mkdir -m 1777 /rootfs/tmp; \
    find /bin /sbin /usr/bin /usr/sbin /usr/local -type f -exec scanelf -BF '%F' {} + | tr '\n' '\0' | xargs -0 -r lddtree -l | sort -u > /tmp/libs.txt; \
    tar -cf /tmp/libs.tar -T /tmp/libs.txt; \
    tar -C /rootfs -xf /tmp/libs.tar; \
    tar -C / -cf /tmp/data.tar bin sbin usr/bin usr/sbin usr/local usr/share/icu usr/share/zoneinfo docker-entrypoint-initdb.d etc/passwd etc/group var/lib/postgresql var/run/postgresql; \
    tar -C /rootfs -xf /tmp/data.tar; \
    touch /rootfs/dev/null; \
    chmod 666 /rootfs/dev/null; \
    chroot /rootfs su-exec postgres initdb -D /tmp/pgdata; \
    echo 'SELECT 1;' | chroot /rootfs su-exec postgres postgres --single -D /tmp/pgdata -c shared_preload_libraries=pg_ukc_scaletozero postgres; \
    rm -rf /rootfs/dev/null /rootfs/tmp/pgdata

FROM scratch

ENV LANG=en_US.utf8
ENV PGDATA=/var/lib/postgresql/data

COPY --from=runtime /rootfs /
