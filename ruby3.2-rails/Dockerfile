# The generated app tree is architecture-independent text, so this stage
# runs natively on whatever the build host is. The gems it installs are
# only needed to run the rails generators and are discarded.
FROM --platform=$BUILDPLATFORM ruby:3.2.2-bookworm AS appgen

ARG RAILS_VERSION=8.1.3
RUN gem install rails -v "$RAILS_VERSION"

# --skip-bundle: `rails new` would otherwise run a full `bundle install` right
# here, natively compiling Puma and nio4r for the build host — only for the
# next instruction to drop Puma from the Gemfile again. Skipping it means the
# app bundle is resolved and installed exactly once, below.
RUN rails new app --minimal --skip-bundle

WORKDIR /app

# Puma ships a C extension (its HTTP/1.1 parser) and pulls in nio4r, another
# C extension; both would otherwise compile from source in the x86_64 `build`
# stage — under QEMU emulation on non-amd64 hosts. WEBrick is pure Ruby, so
# swapping it in removes the only meaningful native compilation left in the
# emulated bundle install. With Puma gone, `rails server` (the Kraftfile cmd)
# selects WEBrick — the only Rack server gem left in the bundle — via Rack's
# handler auto-detection; config/puma.rb is now dead config and is dropped.
# WEBrick is single-threaded and not a production server, which is acceptable
# for this hello-world example.
#
# This is a plain text edit rather than `bundle remove` / `bundle add` because
# those resolve (and `bundle add` installs) on their own, which is exactly the
# duplicated work --skip-bundle just removed. The grep guard fails the build
# loudly if a future Rails changes the generated Gemfile format and the
# substitution silently matches nothing, leaving Puma in the bundle.
RUN sed -i '/^[[:space:]]*gem "puma"/d' Gemfile && \
    ! grep -qE '^[[:space:]]*gem .puma.' Gemfile && \
    printf '\ngem "webrick"\n' >> Gemfile && \
    rm -f config/puma.rb

# The rootfs targets x86_64 regardless of build host, so the lockfile has to
# cover that platform. Resolving with --add-platform *first* writes a lockfile
# for both platforms in a single resolve; the install below then works from
# that lockfile rather than resolving the graph a second time.
RUN bundle lock --add-platform x86_64-linux

# The only gem install in this stage. It has to precede `rails generate`,
# which boots the app and therefore needs the gems present.
RUN bundle install --jobs 4

# `bundle install` resolves for the build host's own platform, so it is what
# would drop x86_64-linux from the lockfile if bundler ever pruned it. That
# would otherwise surface much later — as "your bundle only supports platforms
# [...]" from the emulated x86_64 stage. Fail here, where the cause is obvious.
RUN grep -q 'x86_64-linux' Gemfile.lock || \
    { echo 'ERROR: x86_64-linux was pruned from Gemfile.lock' >&2; exit 1; }

RUN rails generate controller hello

COPY . /app/

# Arch-specific caches must not leak into the rootfs.
RUN rm -rf tmp/cache log/*

# Gem native extensions must be compiled for x86_64, which no Ruby tooling
# can cross-compile, so this is the one stage that has to execute x86_64
# binaries (under QEMU emulation on other hosts).
FROM --platform=linux/x86_64 ruby:3.2.2-bookworm AS build

WORKDIR /app
COPY --from=appgen /app/Gemfile /app/Gemfile.lock ./
RUN bundle install --jobs 4

FROM scratch

# Ruby binary
COPY --from=build /usr/local/bin/ruby /usr/bin/ruby

# Ruby libraries
COPY --from=build /usr/local/lib/ruby /usr/local/lib/ruby

# System libraries
COPY --from=build /usr/local/lib/libruby.so.3.2 /usr/local/lib/libruby.so.3.2
COPY --from=build /lib/x86_64-linux-gnu/libz.so.1 /lib/x86_64-linux-gnu/libz.so.1
COPY --from=build /lib/x86_64-linux-gnu/libgmp.so.10 /lib/x86_64-linux-gnu/libgmp.so.10
COPY --from=build /lib/x86_64-linux-gnu/libcrypt.so.1 /lib/x86_64-linux-gnu/libcrypt.so.1
COPY --from=build /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=build /etc/ld.so.cache /etc/ld.so.cache

# Ruby Gems & Rails contents
COPY --from=build /usr/local/bundle /usr/local/bundle

# System libraries required by Rails
COPY --from=build /lib/x86_64-linux-gnu/libcurses.so /lib/x86_64-linux-gnu/libcurses.so
COPY --from=build /lib/x86_64-linux-gnu/libdl.so.2 /lib/x86_64-linux-gnu/libdl.so.2
COPY --from=build /lib/x86_64-linux-gnu/libffi.so.8 /lib/x86_64-linux-gnu/libffi.so.8
COPY --from=build /lib/x86_64-linux-gnu/libncurses.so /lib/x86_64-linux-gnu/libncurses.so
COPY --from=build /lib/x86_64-linux-gnu/libncursesw.so /lib/x86_64-linux-gnu/libncursesw.so
COPY --from=build /lib/x86_64-linux-gnu/libpthread.so.0 /lib/x86_64-linux-gnu/libpthread.so.0
COPY --from=build /lib/x86_64-linux-gnu/libcrypto.so.3 /lib/x86_64-linux-gnu/libcrypto.so.3
COPY --from=build /lib/x86_64-linux-gnu/libssl.so.3 /lib/x86_64-linux-gnu/libssl.so.3
COPY --from=build /lib/x86_64-linux-gnu/libyaml-0.so.2 /lib/x86_64-linux-gnu/libyaml-0.so.2

# Timezone information
COPY --from=build /usr/share/zoneinfo /usr/share/zoneinfo

# Rails application (arch-independent, generated in the native stage)
COPY --from=appgen /app /app
