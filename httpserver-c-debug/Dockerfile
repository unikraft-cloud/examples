FROM gcc:13.2.0-bookworm AS build

WORKDIR /src

COPY ./http_server.c /src/http_server.c

RUN gcc \
    -Wall -Wextra \
    -fPIC -pie \
    -o /usr/bin/http_server http_server.c

RUN set -xe; \
    apt-get -yqq update; \
    apt-get -yqq install openssh-server strace net-tools pax-utils \
    ;

RUN echo "root:unikraft" | chpasswd

RUN mkdir /run/sshd

RUN set -xe; \
    lddtree --copy-to-tree /rootfs \
      /usr/bin/http_server \
      /usr/sbin/sshd \
      /usr/bin/chown \
      /usr/bin/strace \
      /usr/bin/netstat \
      /usr/bin/su \
      /bin/bash \
      /bin/sh \
      /usr/bin/ls \
      /usr/bin/file \
      /usr/bin/ps \
      /usr/bin/sleep \
      /usr/bin/cat; \
    find /lib/*/security -type f -print0 | xargs -0 lddtree --skip-non-elfs --copy-to-tree /rootfs; \
    tar -C / -cf /tmp/data.tar \
      etc/passwd etc/shadow etc/group \
      etc/ssh run/sshd root/.ssh \
      etc/pam.conf etc/pam.d etc/security etc/login.defs etc/nsswitch.conf \
      usr/lib/file usr/share/misc/magic.mgc; \
    tar -C /rootfs -xf /tmp/data.tar; \
    mkdir /rootfs/dev; \
    mknod -m 666 /rootfs/dev/null c 1 3; \
    chroot /rootfs /usr/sbin/sshd -t; \
    chroot /rootfs /bin/sh -c 'bash -c true && ls / && strace -V && netstat --version && file /usr/bin/file && su -c true'; \
    rm -r /rootfs/dev

FROM scratch

COPY --from=build /rootfs /
COPY ./sshd_config /etc/ssh/sshd_config
COPY ./wrapper.sh /usr/bin/wrapper.sh
