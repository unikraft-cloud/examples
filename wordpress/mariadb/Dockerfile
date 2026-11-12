FROM mariadb:11.7.2-noble AS build

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends pax-utils; \
    rm -rf /var/lib/apt/lists/*

RUN set -xe; \
    mkdir -p /rootfs/tmp; \
    lddtree --copy-to-tree /rootfs \
        /usr/sbin/mariadbd \
        /usr/bin/mariadb \
        /usr/bin/mariadb-tzinfo-to-sql \
        /usr/bin/my_print_defaults \
        /bin/sh \
        /bin/bash \
        /bin/mount \
        /usr/bin/date \
        /usr/bin/gawk \
        /usr/bin/id \
        /usr/bin/mkdir \
        /usr/bin/find \
        /usr/bin/kill \
        /usr/bin/chown \
        /usr/bin/chmod \
        /usr/bin/ls \
        /usr/bin/sed \
        /usr/bin/uname \
        /usr/bin/cat \
        /usr/bin/sleep \
        /usr/bin/pwgen \
        /usr/local/bin/gosu \
        /usr/lib/mysql/plugin/*.so; \
    tar -C / -cf /tmp/data.tar \
        etc/ssl/certs/ca-certificates.crt \
        etc/passwd \
        etc/shadow \
        etc/mysql \
        etc/alternatives/awk \
        etc/alternatives/my.cnf \
        usr/bin/awk \
        usr/bin/mariadb-install-db \
        usr/lib/mysql \
        usr/share/mariadb \
        usr/share/zoneinfo \
        usr/local/bin/docker-entrypoint.sh \
        docker-entrypoint-initdb.d \
        run/mysqld; \
    tar -C /rootfs -xf /tmp/data.tar; \
    find /rootfs -type d -exec chmod 755 {} +; \
    chmod 1777 /rootfs/tmp /rootfs/run/mysqld

COPY ./wrapper.sh /rootfs/usr/local/bin/wrapper.sh
COPY ./50-server.cnf /rootfs/etc/mysql/mariadb.conf.d/50-server.cnf

RUN set -xe; \
    chroot /rootfs /usr/sbin/mariadbd --help --verbose > /dev/null; \
    chroot /rootfs /usr/sbin/mariadbd --print-defaults | grep -q -- --collation-server=utf8mb4_unicode_ci; \
    chroot /rootfs /usr/bin/awk 'BEGIN { exit 0 }'

FROM scratch

COPY --from=build /rootfs /
