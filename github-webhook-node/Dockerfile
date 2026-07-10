FROM --platform=$BUILDPLATFORM node:24-alpine AS build

WORKDIR /app

COPY server.js package*.json ./

RUN npm install --omit=dev

FROM --platform=$BUILDPLATFORM scratch

COPY --from=build /usr/local/bin/node /usr/local/bin/node

COPY --from=build /lib/ld-musl-x86_64.so.1 /lib/ld-musl-x86_64.so.1
COPY --from=build /usr/lib/libstdc++.so.6 /usr/lib/libstdc++.so.6
COPY --from=build /usr/lib/libgcc_s.so.1 /usr/lib/libgcc_s.so.1

COPY --from=build /app/node_modules /app/node_modules
COPY --from=build /app/server.js /app/server.js
