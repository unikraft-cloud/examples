FROM --platform=$BUILDPLATFORM gcc:13.2.0-bookworm AS build

WORKDIR /src

COPY ./http_server.c /src/http_server.c

RUN gcc \
    -Wall -Wextra \
    -fPIC -pie \
    -o /usr/bin/http_server http_server.c

RUN set -xe; \
    apt-get -yqq update; \
    apt-get -yqq install openssh-server strace net-tools \
    ;

RUN echo "root:unikraft" | chpasswd

RUN mkdir /run/sshd

FROM --platform=$BUILDPLATFORM scratch

# Configuration files
COPY --from=build /etc/passwd /etc/passwd
COPY --from=build /etc/shadow /etc/shadow
COPY --from=build /etc/group /etc/group

# Basic binaries
COPY --from=build /usr/sbin/sshd /usr/sbin/sshd
COPY --from=build /usr/bin/chown /usr/bin/chown
COPY --from=build /usr/bin/strace /usr/bin/strace
COPY --from=build /usr/bin/netstat /usr/bin/netstat
COPY --from=build /usr/bin/su /usr/bin/su
COPY --from=build /bin/bash /bin/bash
COPY --from=build /bin/sh /bin/sh

# SSHD configuration
COPY --from=build /etc/ssh /etc/ssh
COPY --from=build /run/sshd /run/sshd
COPY --from=build /root/.ssh /root/.ssh
COPY ./sshd_config /etc/ssh/sshd_config

# Investigation binaries
COPY --from=build /usr/bin/ls /usr/bin/ls
COPY --from=build /usr/bin/file /usr/bin/file
COPY --from=build /usr/bin/ps /usr/bin/ps
COPY --from=build /usr/bin/sleep /usr/bin/sleep
COPY --from=build /usr/bin/cat /usr/bin/cat

# System libraries
COPY --from=build /lib/x86_64-linux-gnu/libaudit.so.1 \
                  /lib/x86_64-linux-gnu/libbz2.so.1.0 \
                  /lib/x86_64-linux-gnu/libcap-ng.so.0 \
                  /lib/x86_64-linux-gnu/libcap.so.2 \
                  /lib/x86_64-linux-gnu/libcom_err.so.2 \
                  /lib/x86_64-linux-gnu/libcrypto.so.3 \
                  /lib/x86_64-linux-gnu/libcrypt.so.1 \
                  /lib/x86_64-linux-gnu/libc.so.6 \
                  /lib/x86_64-linux-gnu/libgcrypt.so.20 \
                  /lib/x86_64-linux-gnu/libgpg-error.so.0 \
                  /lib/x86_64-linux-gnu/libgssapi_krb5.so.2 \
                  /lib/x86_64-linux-gnu/libk5crypto.so.3 \
                  /lib/x86_64-linux-gnu/libkeyutils.so.1 \
                  /lib/x86_64-linux-gnu/libkrb5.so.3 \
                  /lib/x86_64-linux-gnu/libkrb5support.so.0 \
                  /lib/x86_64-linux-gnu/liblz4.so.1 \
                  /lib/x86_64-linux-gnu/liblzma.so.5 \
                  /lib/x86_64-linux-gnu/libmagic.so.1 \
                  /lib/x86_64-linux-gnu/libpam.so.0 \
                  /lib/x86_64-linux-gnu/libpam_misc.so.0 \
                  /lib/x86_64-linux-gnu/libpcre2-8.so.0 \
                  /lib/x86_64-linux-gnu/libproc2.so.0 \
                  /lib/x86_64-linux-gnu/libresolv.so.2 \
                  /lib/x86_64-linux-gnu/libselinux.so.1 \
                  /lib/x86_64-linux-gnu/libsystemd.so.0 \
                  /lib/x86_64-linux-gnu/libtinfo.so.6 \
                  /lib/x86_64-linux-gnu/libunwind-ptrace.so.0 \
                  /lib/x86_64-linux-gnu/libunwind.so.8 \
                  /lib/x86_64-linux-gnu/libunwind-x86_64.so.8 \
                  /lib/x86_64-linux-gnu/libwrap.so.0 \
                  /lib/x86_64-linux-gnu/libz.so.1 \
                  /lib/x86_64-linux-gnu/libzstd.so.1 \
                  /lib/x86_64-linux-gnu/libnsl.so.2 \
                  /lib/x86_64-linux-gnu/libtirpc.so.3 \
                  /lib/x86_64-linux-gnu/
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2

# PAM modules required for SSH / authentication
COPY --from=build /etc/pam.conf /etc/pam.conf
COPY --from=build /etc/pam.d /etc/pam.d
COPY --from=build /lib/x86_64-linux-gnu/security /lib/x86_64-linux-gnu/security

# Security / Authentication configuration files
COPY --from=build /etc/security /etc/security
COPY --from=build /etc/login.defs /etc/login.defs
COPY --from=build /etc/nsswitch.conf /etc/nsswitch.conf

# Application binary
COPY --from=build /usr/bin/http_server /usr/bin/http_server

COPY ./wrapper.sh /usr/bin/wrapper.sh
