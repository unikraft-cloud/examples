FROM --platform=$BUILDPLATFORM node:23-alpine AS build

WORKDIR /app

COPY package*.json /app/

RUN set -xe; \
    npm ci

COPY index.html vite.config.js /app/
COPY src/ /app/src/
COPY public/ /app/public/

FROM --platform=$BUILDPLATFORM scratch

# Node binary
COPY --from=build /usr/local/bin/node /usr/local/bin/node

# System libraries
COPY --from=build /lib/ld-musl-x86_64.so.1 /lib/ld-musl-x86_64.so.1
COPY --from=build /usr/lib/libgcc_s.so.1 /usr/lib/libgcc_s.so.1
COPY --from=build /usr/lib/libstdc++.so.6 /usr/lib/libstdc++.so.6

# Application
COPY --from=build /app /app
