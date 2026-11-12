FROM elixir:1.19.2-slim AS build

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends ca-certificates pax-utils

WORKDIR /src

COPY . .

RUN mix deps.get

RUN mix compile && mix release

COPY ./wrapper.sh /rootfs/usr/bin/wrapper.sh

RUN set -xe; \
    mkdir -p /rootfs/dev /rootfs/tmp; \
    find /usr/local/lib/erlang -type f -print0 | xargs -0 lddtree --skip-non-elfs --copy-to-tree /rootfs; \
    lddtree --copy-to-tree /rootfs /bin/sh /usr/bin/basename /usr/bin/cat /usr/bin/cut /usr/bin/dirname /usr/bin/grep /usr/bin/readlink /usr/bin/sed; \
    tar -C / -cf /tmp/data.tar usr/local/lib/erlang usr/local/bin/erl usr/lib/locale src/_build/dev/rel etc/ssl/certs/ca-certificates.crt; \
    tar -C /rootfs -xf /tmp/data.tar; \
    find /rootfs -type d -exec chmod 755 {} +; \
    chmod 1777 /rootfs/tmp; \
    touch /rootfs/dev/null; \
    chroot /rootfs /usr/bin/wrapper.sh _build/dev/rel/server/bin/server eval '{:ok,_}=Application.ensure_all_started(:crypto)'; \
    rm /rootfs/dev/null

FROM scratch

COPY --from=build /rootfs /
