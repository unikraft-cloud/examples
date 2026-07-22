# Find eligible builder and runner images on Docker Hub. We use Ubuntu/Debian
# instead of Alpine to avoid DNS resolution issues in production.
#
# https://hub.docker.com/r/hexpm/elixir/tags?name=ubuntu
# https://hub.docker.com/_/ubuntu/tags
#
# This file is based on these images:
#
#   - https://hub.docker.com/r/hexpm/elixir/tags - for the build image
#   - https://hub.docker.com/_/debian/tags?name=bookworm-20241202-slim - for the release image
#   - https://pkgs.org/ - resource for finding needed packages
#   - Ex: docker.io/hexpm/elixir:1.17.3-erlang-27.1.2-debian-bookworm-20241202-slim
#
# Compiled .beam files are architecture-independent and none of the app's
# deps ship NIFs, so the whole mix build runs natively on the build host.
# The only x86_64-specific pieces of the release are ERTS and the native
# parts of OTP's own applications (crypto NIF etc.); those are swapped in
# from the x86_64 variant of the same builder image, which is only pulled,
# never run.
ARG ELIXIR_VERSION=1.17.3
ARG OTP_VERSION=27.1.2
ARG DEBIAN_VERSION=bookworm-20241202-slim

ARG BUILDER_IMAGE="docker.io/hexpm/elixir:${ELIXIR_VERSION}-erlang-${OTP_VERSION}-debian-${DEBIAN_VERSION}"
ARG RUNNER_IMAGE="docker.io/debian:${DEBIAN_VERSION}"

# x86_64 ERTS/OTP donor; no code from this stage is ever executed.
FROM --platform=linux/x86_64 ${BUILDER_IMAGE} AS otp-x86

FROM --platform=$BUILDPLATFORM ${BUILDER_IMAGE} AS builder

# install build dependencies ("file" is used to verify the assembled
# release contains only x86_64 native code)
RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential git file \
  && rm -rf /var/lib/apt/lists/*

# prepare build dir
WORKDIR /app

# install hex + rebar
RUN mix local.hex --force \
  && mix local.rebar --force

# set build ENV
ENV MIX_ENV="prod"

# install mix dependencies
COPY mix.exs mix.lock ./
RUN mix deps.get --only $MIX_ENV
RUN mkdir config

# copy compile-time config files before we compile dependencies
# to ensure any relevant config change will trigger the dependencies
# to be re-compiled.
COPY config/config.exs config/${MIX_ENV}.exs config/
RUN mix deps.compile

# esbuild/tailwind download binaries for the build host and only run at
# build time; the assets they emit are architecture-independent.
RUN mix assets.setup

COPY priv priv

COPY lib lib

# Compile the release
RUN mix compile

COPY assets assets

# compile assets
RUN mix assets.deploy

# Changes to config/runtime.exs don't require recompiling the code
COPY config/runtime.exs config/

COPY rel rel
RUN mix release

# Swap the release's ERTS and OTP applications for their x86_64
# counterparts (same OTP build, so the .beam files are identical and only
# the native binaries/NIFs differ).  mix release rewrites erts' bin/erl
# into a location-independent script, which must survive the swap.
# Anything not present in the donor OTP is a hex dep or the app itself,
# i.e. pure .beam code; the final `file` sweep proves no foreign-arch ELF
# slipped through (e.g. if a NIF dependency is ever added).
COPY --from=otp-x86 /usr/local/lib/erlang /otp-x86

RUN set -e; \
    rel="/app/_build/${MIX_ENV}/rel/myapp"; \
    ertsdir=$(cd "$rel" && echo erts-*); \
    test -d "/otp-x86/$ertsdir"; \
    cp "$rel/$ertsdir/bin/erl" /tmp/dyn-erl; \
    rm -rf "$rel/${ertsdir:?}"; \
    cp -a "/otp-x86/$ertsdir" "$rel/"; \
    cp /tmp/dyn-erl "$rel/$ertsdir/bin/erl"; \
    for d in "$rel"/lib/*; do \
        n=$(basename "$d"); \
        if [ -d "/otp-x86/lib/$n" ]; then \
            rm -rf "$d"; \
            cp -a "/otp-x86/lib/$n" "$rel/lib/"; \
        fi; \
    done; \
    if find "$rel" -type f -exec file {} + | grep ELF | grep -v 'x86-64'; then \
        echo "non-x86_64 ELF files remain in release" >&2; \
        exit 1; \
    fi

# Runtime pieces for the final image, assembled natively: amd64 libraries
# are unpacked from prebuilt debs (no maintainer scripts run), the en_US
# locale is compiled with localedef (its output is architecture-
# independent), and the CA bundle is plain data.
FROM --platform=$BUILDPLATFORM debian:bookworm AS runtime-deps

RUN set -xe; \
    dpkg --add-architecture amd64; \
    apt-get -yqq update; \
    apt-get -yqq install --no-install-recommends locales ca-certificates; \
    localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8; \
    mkdir -p /rootfs/usr/lib/locale /rootfs/etc/ssl/certs /rootfs/usr/share/ca-certificates; \
    cp /usr/lib/locale/locale-archive /rootfs/usr/lib/locale/; \
    cp -a /etc/ssl/certs/. /rootfs/etc/ssl/certs/; \
    cp -a /usr/share/ca-certificates/. /rootfs/usr/share/ca-certificates/; \
    cp /etc/ca-certificates.conf /rootfs/etc/; \
    mkdir /debs; \
    cd /debs; \
    apt-get -yqq download \
        libstdc++6:amd64 \
        libssl3:amd64 \
        libncursesw6:amd64 \
        libncurses6:amd64; \
    for deb in *.deb; do dpkg-deb -x "$deb" /rootfs; done; \
    rm -rf /rootfs/usr/share/doc /rootfs/usr/share/lintian; \
    # some debs (ncurses) still ship pre-usr-merge paths; the final image's
    # /lib is a symlink to usr/lib, and COPY cannot overlay a directory
    # onto a symlink, so fold the tree into the merged layout
    for d in lib lib64 bin sbin; do \
        if [ -d "/rootfs/$d" ] && [ ! -L "/rootfs/$d" ]; then \
            mkdir -p "/rootfs/usr/$d"; \
            cp -a "/rootfs/$d/." "/rootfs/usr/$d/"; \
            rm -rf "/rootfs/${d:?}"; \
        fi; \
    done

# start a new build stage so that the final image will only contain
# the compiled release and other runtime necessities
FROM --platform=linux/x86_64 ${RUNNER_IMAGE} AS final

COPY --from=runtime-deps /rootfs/ /

# Set the locale (compiled into the locale-archive copied above)
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

WORKDIR "/app"
RUN chown nobody /app

# set runner ENV
ENV MIX_ENV="prod"

# Only copy the final release from the build stage
COPY --from=builder --chown=nobody:root /app/_build/${MIX_ENV}/rel/myapp ./

USER nobody

# If using an environment that doesn't automatically reap zombie processes, it is
# advised to add an init process such as tini via `apt-get install`
# above and adding an entrypoint. See https://github.com/krallin/tini for details
# ENTRYPOINT ["/tini", "--"]
