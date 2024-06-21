FROM --platform=$BUILDPLATFORM elixir:1.16.2-slim AS build

WORKDIR /src

COPY . .

RUN mix deps.get

RUN MIX_TARGET=$TARGETARCH mix compile && mix release

FROM alpine:3 AS sys

RUN set -xe; \
    mkdir -p /target/etc; \
    mkdir -p /blank; \
    apk --no-cache add \
      ca-certificates \
      tzdata \
    ; \
    update-ca-certificates; \
    ln -sf /usr/share/zoneinfo/Etc/UTC /target/etc/localtime; \
    echo "Etc/UTC" > /target/etc/timezone;

FROM --platform=$TARGETPLATFORM elixir:1.16.2-slim AS runtime

FROM scratch

COPY --from=sys /target/etc /etc
COPY --from=sys /usr/share/zoneinfo/UTC /usr/share/zoneinfo/UTC
COPY --from=sys /usr/share/zoneinfo/Etc/UTC /usr/share/zoneinfo/Etc/UTC
COPY --from=sys /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=sys /blank /tmp

COPY --from=runtime /lib/x86_64-linux-gnu/libc.so.6 \
                    /lib/x86_64-linux-gnu/libgcc_s.so.1 \
                    /lib/x86_64-linux-gnu/libm.so.6 \
                    /lib/x86_64-linux-gnu/libsctp.so.1 \
                    /lib/x86_64-linux-gnu/libstdc++.so.6 \
                    /lib/x86_64-linux-gnu/libtinfo.so.6 \
                    /lib/x86_64-linux-gnu/libcrypto.so.3 \
                    /lib/x86_64-linux-gnu/libselinux.so.1 \
                    /lib/x86_64-linux-gnu/libc.so.6 \
                    /lib/x86_64-linux-gnu/libpcre2-8.so.0 \
                    /lib/x86_64-linux-gnu/libacl.so.1 \
                    /lib/x86_64-linux-gnu/

COPY --from=runtime /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2

COPY --from=runtime /usr/local/lib/erlang /usr/local/lib/erlang
COPY --from=runtime /usr/local/lib/elixir /usr/local/lib/elixir

# Erlang and Elixir-related executables
COPY --from=runtime /usr/local/bin /usr/local/bin

COPY --from=runtime /usr/lib/locale /usr/lib/locale

COPY --from=runtime /usr/bin/dirname \
                    /usr/bin/basename \
                    /usr/bin/readlink \
                    /usr/bin/env \
                    /usr/bin/

COPY --from=runtime /bin/rm \
                    /bin/mknod \
                    /bin/bash \
                    /bin/sh \
                    /bin/

COPY --from=build /root /root

COPY --from=build /src/deps /src/deps
COPY --from=build /src/_build /src/_build
COPY --from=build /src/lib /src/lib
COPY --from=build /src/mix.exs /src/mix.exs
COPY --from=build /src/mix.lock /src/mix.lock
COPY --from=build /usr/bin/cut /usr/bin/cut
COPY --from=build /usr/bin/sed /usr/bin/sed
COPY --from=build /usr/bin/cat /usr/bin/cat
COPY --from=build /usr/bin/grep /usr/bin/grep

COPY ./wrapper.sh /usr/bin/wrapper.sh
