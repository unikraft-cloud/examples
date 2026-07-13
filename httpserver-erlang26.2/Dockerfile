# Compile the BEAM bytecode natively on the build host — the .beam file is
# architecture-independent.
FROM --platform=$BUILDPLATFORM erlang:26.2.3.0-slim as build

WORKDIR /src

#COPY ./helloworld.erl .
COPY ./http_server.erl .

RUN /usr/local/bin/erl -compile http_server

# Erlang runtime and x86_64 system libraries for the final image (copy-only,
# nothing runs under emulation).
FROM --platform=linux/x86_64 erlang:26.2.3.0-slim AS runtime

FROM --platform=$BUILDPLATFORM alpine:3 AS sys

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

FROM scratch

COPY --from=sys /target/etc /etc
COPY --from=sys /usr/share/zoneinfo/UTC /usr/share/zoneinfo/UTC
COPY --from=sys /usr/share/zoneinfo/Etc/UTC /usr/share/zoneinfo/Etc/UTC
COPY --from=sys /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=sys /blank /tmp

COPY --from=runtime /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=runtime /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=runtime /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=runtime /lib/x86_64-linux-gnu/libsctp.so.1 /lib/x86_64-linux-gnu/libsctp.so.1
COPY --from=runtime /lib/x86_64-linux-gnu/libstdc++.so.6 /lib/x86_64-linux-gnu/libstdc++.so.6
COPY --from=runtime /lib/x86_64-linux-gnu/libtinfo.so.6 /lib/x86_64-linux-gnu/libtinfo.so.6
COPY --from=runtime /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2

COPY --from=runtime /lib/x86_64-linux-gnu/libselinux.so.1 /lib/x86_64-linux-gnu/libselinux.so.1
COPY --from=runtime /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=runtime /lib/x86_64-linux-gnu/libpcre2-8.so.0 /lib/x86_64-linux-gnu/libpcre2-8.so.0
COPY --from=runtime /bin/rm /bin/rm
COPY --from=runtime /bin/mknod /bin/mknod

COPY --from=runtime /usr/local/bin/erl /usr/bin/erl
COPY --from=runtime /usr/local/lib/erlang /usr/local/lib/erlang

COPY --from=runtime /usr/bin/dirname /usr/bin/dirname
COPY --from=runtime /usr/bin/basename /usr/bin/basename

COPY --from=runtime /bin/bash /bin/bash
COPY --from=runtime /bin/sh /bin/sh

COPY --from=build /src/http_server.beam /usr/src/http_server.beam

COPY ./wrapper.sh /usr/bin/wrapper.sh
