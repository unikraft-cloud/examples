FROM mysql:8.0-oraclelinux9 AS build

RUN set -xe; \
    microdnf install -y oracle-epel-release-el9; \
    microdnf --enablerepo=ol9_developer_EPEL install -y pax-utils; \
    microdnf clean all

RUN set -xe; \
    mkdir -p -m 1777 /rootfs/tmp; \
    mkdir -p /rootfs/docker-entrypoint-initdb.d; \
    lddtree -l \
        /usr/sbin/mysqld \
        /usr/bin/mysql \
        /usr/bin/mysql_tzinfo_to_sql \
        /usr/bin/my_print_defaults \
        /usr/bin/mysqladmin \
        /usr/bin/openssl \
        /usr/local/bin/gosu \
        /usr/bin/coreutils \
        /usr/bin/bash \
        /usr/bin/env \
        /usr/bin/mkdir \
        /usr/bin/cat \
        /usr/bin/chmod \
        /usr/bin/find \
        /usr/bin/dirname \
        /usr/bin/date \
        /usr/bin/gawk \
        /usr/bin/sed \
        /usr/bin/ln \
        /usr/bin/chown \
        /usr/bin/id \
        /usr/bin/ls \
        /usr/bin/mktemp \
        /usr/lib*/mysql/plugin/*.so \
        | xargs realpath -s | sort -u > /tmp/libs.txt; \
    tar -chf /tmp/libs.tar -T /tmp/libs.txt; \
    tar -C /rootfs -xf /tmp/libs.tar; \
    tar -C / -cf /tmp/data.tar \
        etc/passwd \
        etc/shadow \
        etc/group \
        etc/gshadow \
        etc/my.cnf \
        etc/my.cnf.d \
        etc/mysql \
        usr/bin/awk \
        usr/bin/sh \
        usr/lib*/mysql/plugin \
        usr/lib*/mysql/private \
        usr/share/mysql-8.0 \
        usr/share/zoneinfo \
        usr/local/bin/docker-entrypoint.sh \
        var/lib/mysql \
        var/run/mysqld; \
    tar -C /rootfs -xf /tmp/data.tar; \
    ln -s usr/bin /rootfs/bin; \
    chroot /rootfs /usr/sbin/mysqld --help --verbose > /dev/null; \
    chroot /rootfs /bin/sh -c 'awk "BEGIN { exit 0 }"'; \
    chroot /rootfs /usr/bin/env bash -c 'test -x /bin/bash'

FROM scratch

COPY --from=build /rootfs /
COPY ./wrapper.sh /usr/local/bin/wrapper.sh
