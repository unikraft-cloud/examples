FROM debian:bookworm AS build

RUN set -xe; \
    apt-get -yqq update; \
    apt-get -yqq install vsftpd; \
    apt-get -yqq install --no-install-recommends pax-utils; \
    rm -rf /var/lib/apt/lists/*

RUN set -xe; \
    echo "root:rootpass" | chpasswd; \
    mkdir -p /var/run/vsftpd/empty; \
    touch /var/log/vsftpd.log; \
    echo "root" > /etc/vsftpd.userlist; \
    sed -i '/^root/d' /etc/ftpusers

RUN set -xe; \
    mkdir -p /rootfs/tmp; \
    lddtree --copy-to-tree /rootfs \
        /usr/sbin/vsftpd \
        /bin/sh \
        /bin/mkdir \
        /bin/chown \
        /bin/echo \
        /usr/bin/tail \
        /lib/*/libnss_files.so.2 \
        /lib/*/libnss_compat.so.2 \
        /lib/*/security/*.so; \
    tar -C / -cf /tmp/data.tar \
        etc/passwd \
        etc/group \
        etc/shadow \
        etc/ftpusers \
        etc/vsftpd.userlist \
        etc/pam.d \
        etc/nsswitch.conf \
        etc/shells \
        etc/login.defs \
        var/run/vsftpd/empty \
        var/log/vsftpd.log; \
    tar -C /rootfs -xf /tmp/data.tar; \
    find /rootfs -type d -exec chmod 755 {} +; \
    chmod 1777 /rootfs/tmp

COPY ./vsftpd.conf /rootfs/etc/vsftpd/vsftpd.conf
COPY --chmod=755 ./wrapper.sh /rootfs/wrapper.sh

RUN set -xe; \
    chroot /rootfs /usr/sbin/vsftpd -v 0>&1; \
    chroot /rootfs /bin/sh -c 'mkdir --version && chown --version && echo --version && tail --version' > /dev/null

FROM scratch

COPY --from=build /rootfs /
