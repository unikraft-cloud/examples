FROM erlang:26.2.3.0-slim AS build

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends ca-certificates pax-utils

WORKDIR /src

COPY ./http_server.erl .

RUN erl -compile http_server

COPY ./wrapper.sh /rootfs/usr/bin/wrapper.sh

RUN set -xe; \
    mkdir -p /rootfs/dev /rootfs/tmp /rootfs/usr/src; \
    find /usr/local/lib/erlang -type f -print0 | xargs -0 lddtree --skip-non-elfs --copy-to-tree /rootfs; \
    lddtree --copy-to-tree /rootfs /bin/sh /bin/rm /bin/mknod /usr/bin/dirname /usr/bin/basename; \
    tar -C / -cf /tmp/data.tar usr/local/lib/erlang usr/local/bin/erl etc/ssl/certs/ca-certificates.crt; \
    tar -C /rootfs -xf /tmp/data.tar; \
    find /rootfs -type d -exec chmod 755 {} +; \
    chmod 1777 /rootfs/tmp; \
    cp http_server.beam /rootfs/usr/src/; \
    touch /rootfs/dev/null; \
    chroot /rootfs /usr/local/bin/erl -noshell -eval 'ok = crypto:start(), halt().'; \
    rm /rootfs/dev/null

FROM scratch

COPY --from=build /rootfs /
