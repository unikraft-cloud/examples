# Build the app natively on the build host — the standalone output is
# architecture-independent JavaScript.
FROM --platform=$BUILDPLATFORM node:21-alpine AS build

WORKDIR /usr/src

COPY . /usr/src/

RUN set -xe; \
    npm install; \
    npm run build

# Node binary and system libraries for the target architecture.
FROM --platform=linux/x86_64 node:21-alpine AS node

FROM scratch

# Node binary
COPY --from=node /usr/local/bin/node /usr/bin/node

# System libraries
COPY --from=node /lib/ld-musl-x86_64.so.1 /lib/ld-musl-x86_64.so.1
COPY --from=node /usr/lib/libgcc_s.so.1 /usr/lib/libgcc_s.so.1
COPY --from=node /usr/lib/libstdc++.so.6 /usr/lib/libstdc++.so.6

# Distribution configuration
COPY --from=node /etc/os-release /etc/os-release

# NextJS
COPY --from=build /usr/src/.next/standalone /usr/src/
COPY --from=build /usr/src/.next/static /usr/src/.next/static
COPY ./public /usr/src/public
