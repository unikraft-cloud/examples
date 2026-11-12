FROM perl:5.42.0-bookworm AS build

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends pax-utils

RUN set -xe; \
    cpanm HTTP::Daemon@6.17

COPY ./server.pl /rootfs/usr/src/server.pl

RUN set -xe; \
    mkdir -p /rootfs/tmp; \
    lddtree --copy-to-tree /rootfs /usr/local/bin/perl; \
    find /usr/local/lib/perl5 -type f -print0 | xargs -0 lddtree --skip-non-elfs --copy-to-tree /rootfs; \
    tar -C / -cf /tmp/data.tar usr/local/lib/perl5; \
    tar -C /rootfs -xf /tmp/data.tar; \
    find /rootfs -type d -exec chmod 755 {} +; \
    chmod 1777 /rootfs/tmp; \
    chroot /rootfs /usr/local/bin/perl -c /usr/src/server.pl

FROM scratch

COPY --from=build /rootfs /
