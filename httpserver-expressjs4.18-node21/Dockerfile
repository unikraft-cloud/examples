# Install dependencies natively on the build host — express is pure
# JavaScript.
FROM --platform=$BUILDPLATFORM node:21-alpine AS build

WORKDIR /usr/src

COPY . /usr/src/

RUN npm install

# Node binary and system libraries for the target architecture (copy-only,
# nothing runs under emulation).
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

# Express.js
COPY --from=build /usr/src/node_modules /usr/src/node_modules
COPY --from=build /usr/src/app/index.js /usr/src/server.js
