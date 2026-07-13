# Install dependencies natively on the build host — they are pure JavaScript.
FROM --platform=$BUILDPLATFORM node:24-alpine AS build

WORKDIR /app

COPY server.js package*.json ./

RUN npm install --omit=dev

# Node binary and system libraries for the target architecture (copy-only,
# nothing runs under emulation).
FROM --platform=linux/x86_64 node:24-alpine AS node

FROM scratch

COPY --from=node /usr/local/bin/node /usr/local/bin/node

COPY --from=node /lib/ld-musl-x86_64.so.1 /lib/ld-musl-x86_64.so.1
COPY --from=node /usr/lib/libstdc++.so.6 /usr/lib/libstdc++.so.6
COPY --from=node /usr/lib/libgcc_s.so.1 /usr/lib/libgcc_s.so.1

COPY --from=build /app/node_modules /app/node_modules
COPY --from=build /app/server.js /app/server.js
