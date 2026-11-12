FROM ruby:3.2.2-bookworm AS build

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends pax-utils

COPY ./server.rb /rootfs/src/server.rb

RUN set -xe; \
    mkdir -p /rootfs/tmp; \
    lddtree --copy-to-tree /rootfs /usr/local/bin/ruby; \
    find /usr/local/lib/ruby -type f -print0 | xargs -0 lddtree --skip-non-elfs --copy-to-tree /rootfs; \
    tar -C / -cf /tmp/data.tar usr/local/lib/ruby; \
    tar -C /rootfs -xf /tmp/data.tar; \
    find /rootfs -type d -exec chmod 755 {} +; \
    chmod 1777 /rootfs/tmp; \
    chroot /rootfs /usr/local/bin/ruby -rfiddle -e 'Dir["/usr/local/lib/ruby/**/*.so"].each { |f| Fiddle.dlopen(f) }'

FROM scratch

COPY --from=build /rootfs /
