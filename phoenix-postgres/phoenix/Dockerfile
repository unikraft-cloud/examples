ARG ELIXIR_VERSION=1.17.3
ARG OTP_VERSION=27.1.2
ARG DEBIAN_VERSION=bookworm-20241202-slim

ARG BUILDER_IMAGE="docker.io/hexpm/elixir:${ELIXIR_VERSION}-erlang-${OTP_VERSION}-debian-${DEBIAN_VERSION}"

FROM ${BUILDER_IMAGE} AS builder

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential git pax-utils \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /src

RUN mix local.hex --force \
  && mix local.rebar --force

ENV MIX_ENV="prod"

COPY mix.exs mix.lock ./
RUN mix deps.get --only $MIX_ENV
RUN mkdir config

COPY config/config.exs config/${MIX_ENV}.exs config/
RUN mix deps.compile

RUN mix assets.setup

COPY priv priv

COPY lib lib

RUN mix compile

COPY assets assets

RUN mix assets.deploy

COPY config/runtime.exs config/

COPY rel rel
RUN mix release --path /app

RUN set -xe; \
    mkdir -p /rootfs/dev /rootfs/tmp; \
    find /app -type f -print0 | xargs -0 lddtree --skip-non-elfs --copy-to-tree /rootfs; \
    lddtree --copy-to-tree /rootfs /bin/sh /usr/bin/awk /usr/bin/basename /usr/bin/cat /usr/bin/cut /usr/bin/date /usr/bin/dd /usr/bin/dirname /usr/bin/grep /usr/bin/mkdir /usr/bin/od /usr/bin/readlink /usr/bin/sed; \
    tar -C / -cf /tmp/data.tar app usr/lib/locale/C.utf8 etc/ssl/certs/ca-certificates.crt; \
    tar -C /rootfs -xf /tmp/data.tar; \
    find /rootfs -type d -exec chmod 755 {} +; \
    chmod 1777 /rootfs/tmp; \
    touch /rootfs/dev/null; \
    DATABASE_URL=ecto://localhost/myapp SECRET_KEY_BASE=unused chroot /rootfs /app/bin/myapp eval '{:ok,_}=Application.ensure_all_started(:crypto)'; \
    rm -rf /rootfs/app/tmp; \
    rm /rootfs/dev/null

FROM scratch

ENV LANG=C.UTF-8

COPY --from=builder /rootfs /
