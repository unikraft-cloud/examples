FROM --platform=$BUILDPLATFORM node:23 AS build

WORKDIR /app

COPY package*.json /app/

RUN set -xe; \
    npm ci

COPY . /app/

RUN set -xe; \
    npm run build

# The deployed server runs with NODE_ENV=production and never loads vite
# (dev mode is unsupported in the image: src/ is not shipped), so only the
# production dependencies are installed for the final image.  They are pure
# JS, so this natively-built tree is valid for the x86_64 rootfs.
RUN set -xe; \
    npm ci --omit=dev

# x86_64 node binary and its musl libraries; pulled, never run.
FROM --platform=linux/x86_64 node:23-alpine3.20 AS runtime

FROM scratch

# Node binary
COPY --from=runtime /usr/local/bin/node /usr/local/bin/node

# System libraries
COPY --from=runtime /lib/ld-musl-x86_64.so.1 /lib/ld-musl-x86_64.so.1
COPY --from=runtime /usr/lib/libgcc_s.so.1 /usr/lib/libgcc_s.so.1
COPY --from=runtime /usr/lib/libstdc++.so.6 /usr/lib/libstdc++.so.6

COPY --from=build /app/dist /app/dist
COPY --from=build /app/node_modules /app/node_modules
COPY --from=build /app/package.json /app/package.json
COPY --from=build /app/server.js /app/server.js
COPY --from=build /app/index.html /app/index.html
