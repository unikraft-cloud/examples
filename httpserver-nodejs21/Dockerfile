FROM node:21-alpine AS node

FROM scratch

# Node binary
COPY --from=node /usr/local/bin/node /usr/bin/node

# System libraries
COPY --from=node /lib/ld-musl-x86_64.so.1 /lib/ld-musl-x86_64.so.1
COPY --from=node /usr/lib/libgcc_s.so.1 /usr/lib/libgcc_s.so.1
COPY --from=node /usr/lib/libstdc++.so.6 /usr/lib/libstdc++.so.6

# Node HTTP server
COPY ./server.js /usr/src/server.js
