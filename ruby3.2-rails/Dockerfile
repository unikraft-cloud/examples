FROM --platform=$BUILDPLATFORM ruby:3.2.2-bookworm AS build

RUN gem install rails
RUN rails new app

WORKDIR /app
RUN rails generate controller hello

COPY . /app/

FROM --platform=$BUILDPLATFORM scratch

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

# Rails application
COPY --from=build /app /app
