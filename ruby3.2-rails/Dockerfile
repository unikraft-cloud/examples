FROM ruby:3.2.2-bookworm AS build

RUN gem install rails
RUN rails new app

WORKDIR /app
RUN rails generate controller hello

COPY . /app/

FROM scratch

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
