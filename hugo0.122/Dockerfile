# Download the (target-architecture) hugo release natively on the build host.
FROM --platform=$BUILDPLATFORM debian:bookworm-slim AS build

ARG HUGO_VERSION=0.160.0

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends ca-certificates curl; \
    curl -fsSL "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz" \
      | tar -xz -C /usr/local/bin hugo; \
    rm -rf /var/lib/apt/lists/*

# x86_64 system libraries for the final image (copy-only, nothing runs under
# emulation).
FROM --platform=linux/x86_64 debian:bookworm-slim AS libs

FROM scratch

# Binary executable
COPY --from=build /usr/local/bin/hugo /usr/bin/hugo

# System libraries
COPY --from=libs /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=libs /lib/x86_64-linux-gnu/libdl.so.2 /lib/x86_64-linux-gnu/libdl.so.2
COPY --from=libs /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=libs /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=libs /lib/x86_64-linux-gnu/libpthread.so.0 /lib/x86_64-linux-gnu/libpthread.so.0
COPY --from=libs /lib/x86_64-linux-gnu/libresolv.so.2 /lib/x86_64-linux-gnu/libresolv.so.2
COPY --from=libs /lib/x86_64-linux-gnu/libstdc++.so.6 /lib/x86_64-linux-gnu/libstdc++.so.6
COPY --from=libs /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2

# Site
COPY ./site /site
