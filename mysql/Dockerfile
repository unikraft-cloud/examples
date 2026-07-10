FROM --platform=$BUILDPLATFORM mysql:8.0-debian AS build

FROM --platform=$BUILDPLATFORM scratch

# MySQL binary
COPY --from=build /usr/sbin/mysqld /usr/sbin/mysqld

# MySQL support binaries
COPY --from=build /usr/bin/mysql \
                  /usr/bin/mysql_tzinfo_to_sql \
                  /usr/bin/my_print_defaults \
                  /usr/bin/

# MySQL support files
COPY --from=build --chown=root:root /var/run/mysqld /var/run/mysqld
COPY --from=build --chown=root:root /etc/mysql /etc/mysql
COPY --from=build --chown=root:root /usr/lib/mysql /usr/lib/mysql
COPY --from=build --chown=root:root /usr/share/mysql-8.0 /usr/share/mysql-8.0
COPY --from=build --chown=root:root /var/lib/mysql /var/lib/mysql

# MySQL libraries
COPY --from=build /lib/x86_64-linux-gnu/libssl.so.3 \
                  /lib/x86_64-linux-gnu/libcrypto.so.3 \
                  /lib/x86_64-linux-gnu/libz.so.1 \
                  /lib/x86_64-linux-gnu/libaio.so.1 \
                  /lib/x86_64-linux-gnu/libnuma.so.1 \
                  /lib/x86_64-linux-gnu/libstdc++.so.6 \
                  /lib/x86_64-linux-gnu/libm.so.6 \
                  /lib/x86_64-linux-gnu/libgcc_s.so.1 \
                  /lib/x86_64-linux-gnu/libc.so.6 \
                  /lib/x86_64-linux-gnu/

# Loader
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2

# Binaries
COPY --from=build /bin/sh /bin/sh
COPY --from=build /bin/bash /bin/bash
COPY --from=build /usr/bin/env /usr/bin/env
COPY --from=build /usr/bin/mkdir /usr/bin/mkdir
COPY --from=build /usr/bin/cat /usr/bin/cat
COPY --from=build /usr/bin/chmod /usr/bin/chmod
COPY --from=build /usr/bin/find /usr/bin/find
COPY --from=build /usr/bin/dirname /usr/bin/dirname

# Additional binaries needed by docker-entrypoint.sh
COPY --from=build /usr/local/bin/gosu /usr/local/bin/gosu
COPY --from=build /usr/bin/mysqladmin /usr/bin/mysqladmin
COPY --from=build /usr/bin/openssl /usr/bin/openssl
COPY --from=build /bin/date /bin/date
COPY --from=build /usr/bin/awk /usr/bin/awk
COPY --from=build /bin/sed /bin/sed
COPY --from=build /bin/ln /bin/ln
COPY --from=build /bin/chown /bin/chown
COPY --from=build /usr/bin/id /usr/bin/id
COPY --from=build /bin/ls /bin/ls
COPY --from=build /usr/bin/mktemp /usr/bin/mktemp

# Support files
COPY --from=build /etc/alternatives /etc/alternatives
COPY --from=build /usr/share/zoneinfo /usr/share/zoneinfo

# Libraries for support binaries (Standard GNU/Linux tools)
COPY --from=build /lib/x86_64-linux-gnu/libpcre2-8.so.0 \
                  /lib/x86_64-linux-gnu/libselinux.so.1 \
                  /lib/x86_64-linux-gnu/libtinfo.so.6 \
                  /lib/x86_64-linux-gnu/libacl.so.1 \
                  /lib/x86_64-linux-gnu/libresolv.so.2 \
                  /lib/x86_64-linux-gnu/

# Required empty directory
RUN mkdir -p /docker-entrypoint-initdb.d

# User database
COPY --from=build /etc/passwd /etc/passwd
COPY --from=build /etc/shadow /etc/shadow
COPY --from=build /etc/group /etc/group
COPY --from=build /etc/gshadow /etc/gshadow

# Entrypoint script
COPY --from=build /usr/local/bin/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

# Wrapper script
COPY ./wrapper.sh /usr/local/bin/wrapper.sh

