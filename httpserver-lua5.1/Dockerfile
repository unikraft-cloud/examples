FROM debian:bookworm AS build

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
      build-essential \
      ca-certificates \
      libssl-dev \
      liblua5.1-0-dev \
      lua5.1 \
      luarocks \
      m4 \
      pax-utils \
      unzip; \
    luarocks --lua-version=5.1 install luasocket 3.1.0-1; \
    luarocks --lua-version=5.1 install http 0.4-0

COPY ./http_server.lua /rootfs/http_server.lua

RUN set -xe; \
    mkdir -p /rootfs/tmp /rootfs/usr/lib; \
    ln -s usr/lib /rootfs/lib; \
    lddtree --copy-to-tree /rootfs /usr/bin/lua; \
    find /usr/local/lib/lua -type f -print0 | xargs -0 lddtree --skip-non-elfs --copy-to-tree /rootfs; \
    tar -C / -cf /tmp/data.tar usr/local/share/lua usr/local/lib/lua; \
    tar -C /rootfs -xf /tmp/data.tar; \
    find /rootfs -type d -exec chmod 755 {} +; \
    chmod 1777 /rootfs/tmp; \
    chroot /rootfs /usr/bin/lua -e 'require "socket"; require "http.server"'

FROM scratch

COPY --from=build /rootfs /
