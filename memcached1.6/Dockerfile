FROM --platform=$BUILDPLATFORM memcached:1.6.23-bookworm AS build

FROM --platform=$BUILDPLATFORM scratch

# Binary executable
COPY --from=build /usr/local/bin/memcached /usr/bin/memcached

# System libraryes
COPY --from=build /lib/x86_64-linux-gnu/libssl.so.3 /lib/x86_64-linux-gnu/libssl.so.3
COPY --from=build /lib/x86_64-linux-gnu/libcrypto.so.3 /lib/x86_64-linux-gnu/libcrypto.so.3
COPY --from=build /lib/x86_64-linux-gnu/libevent-2.1.so.7 /lib/x86_64-linux-gnu/libevent-2.1.so.7
COPY --from=build /lib/x86_64-linux-gnu/libsasl2.so.2 /lib/x86_64-linux-gnu/libsasl2.so.2
COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2

# Configuration files
COPY --from=build /etc/passwd /etc/passwd
