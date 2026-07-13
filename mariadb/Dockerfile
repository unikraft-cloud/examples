FROM --platform=linux/x86_64 mariadb:11.7.2-noble AS build

FROM scratch

COPY --from=build /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

# MariaDB binary
COPY --from=build /usr/sbin/mariadbd /usr/sbin/mariadbd

# MariaDB support binaries
COPY --from=build /usr/bin/mariadb \
                  /usr/bin/mariadb-install-db \
                  /usr/bin/mariadb-tzinfo-to-sql \
                  /usr/bin/my_print_defaults \
                  /usr/bin/

# MariaDB support files
COPY --from=build /run/mysqld /run/mysqld
COPY --from=build /etc/mysql /etc/mysql
COPY --from=build /usr/lib/mysql /usr/lib/mysql
COPY --from=build /usr/share/mariadb /usr/share/mariadb

# MariaDB libraries
COPY --from=build /lib/x86_64-linux-gnu/libpcre2-8.so.0 \
                  /lib/x86_64-linux-gnu/libcrypt.so.1 \
                  /lib/x86_64-linux-gnu/liburing.so.2 \
                  /lib/x86_64-linux-gnu/libsystemd.so.0 \
                  /lib/x86_64-linux-gnu/libz.so.1 \
                  /lib/x86_64-linux-gnu/libssl.so.3 \
                  /lib/x86_64-linux-gnu/libcrypto.so.3 \
                  /lib/x86_64-linux-gnu/libstdc++.so.6 \
                  /lib/x86_64-linux-gnu/libm.so.6 \
                  /lib/x86_64-linux-gnu/libgcc_s.so.1 \
                  /lib/x86_64-linux-gnu/libc.so.6 \
                  /lib/x86_64-linux-gnu/libcap.so.2 \
                  /lib/x86_64-linux-gnu/libgcrypt.so.20 \
                  /lib/x86_64-linux-gnu/liblz4.so.1 \
                  /lib/x86_64-linux-gnu/liblzma.so.5 \
                  /lib/x86_64-linux-gnu/libzstd.so.1 \
                  /lib/x86_64-linux-gnu/libgpg-error.so.0 \
                  /lib/x86_64-linux-gnu/libedit.so.2 \
                  /lib/x86_64-linux-gnu/libncurses.so.6 \
                  /lib/x86_64-linux-gnu/libtinfo.so.6 \
                  /lib/x86_64-linux-gnu/libbsd.so.0 \
                  /lib/x86_64-linux-gnu/libmd.so.0 \
                  /lib/x86_64-linux-gnu/

# Loader
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2

# User database
COPY --from=build /etc/passwd /etc/passwd
COPY --from=build /etc/shadow /etc/shadow

# Entrypoint scripts
COPY --from=build /usr/local/bin/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
COPY --from=build /docker-entrypoint-initdb.d /docker-entrypoint-initdb.d

# Support binaries for entrypoint script
COPY --from=build /bin/sh /bin/sh
COPY --from=build /bin/bash /bin/bash
COPY --from=build /usr/bin/date /usr/bin/date
COPY --from=build /usr/bin/awk /usr/bin/awk
COPY --from=build /usr/bin/id /usr/bin/id
COPY --from=build /usr/bin/mkdir /usr/bin/mkdir
COPY --from=build /usr/bin/find /usr/bin/find
COPY --from=build /usr/bin/kill /usr/bin/kill
COPY --from=build /usr/bin/chown /usr/bin/chown
COPY --from=build /usr/bin/chmod /usr/bin/chmod
COPY --from=build /usr/bin/ls /usr/bin/ls
COPY --from=build /usr/bin/sed /usr/bin/sed
COPY --from=build /usr/bin/uname /usr/bin/uname
COPY --from=build /usr/bin/cat /usr/bin/cat
COPY --from=build /usr/bin/sleep /usr/bin/sleep
COPY --from=build /usr/bin/pwgen /usr/bin/pwgen
COPY --from=build /usr/local/bin/gosu /usr/local/bin/gosu
COPY --from=build /bin/mount /bin/mount

# Support files
COPY --from=build /etc/alternatives /etc/alternatives
COPY --from=build /usr/share/zoneinfo /usr/share/zoneinfo

# Libraries for support binaries
COPY --from=build /lib/x86_64-linux-gnu/libtinfo.so.6 \
                  /lib/x86_64-linux-gnu/libc.so.6 \
                  /lib/x86_64-linux-gnu/libsigsegv.so.2 \
                  /lib/x86_64-linux-gnu/libreadline.so.8 \
                  /lib/x86_64-linux-gnu/libmpfr.so.6 \
                  /lib/x86_64-linux-gnu/libgmp.so.10 \
                  /lib/x86_64-linux-gnu/libm.so.6 \
                  /lib/x86_64-linux-gnu/libselinux.so.1 \
                  /lib/x86_64-linux-gnu/libacl.so.1 \
                  /lib/x86_64-linux-gnu/libmount.so.1 \
                  /lib/x86_64-linux-gnu/libblkid.so.1 \
                  /lib/x86_64-linux-gnu/

# Wrapper script
COPY ./wrapper.sh /usr/local/bin/wrapper.sh

# Mariadb configuration file
COPY ./50-server.cnf /etc/mysql/mariadb.conf.d/50-server.cnf
