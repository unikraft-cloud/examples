FROM --platform=$BUILDPLATFORM node:22-alpine AS base

WORKDIR /app

COPY package.json /app

RUN npm install

FROM --platform=$BUILDPLATFORM base AS build

COPY . /app

RUN npm run build; \
    npm prune --production

RUN <<EOF cat >> /app/build/package.json
{"type": "module"}
EOF

FROM --platform=$BUILDPLATFORM scratch

# Node binary
COPY --from=build /usr/local/bin/node /usr/bin/node

# System libraries
COPY --from=build /lib/ld-musl-x86_64.so.1 /lib/ld-musl-x86_64.so.1
COPY --from=build /usr/lib/libgcc_s.so.1 /usr/lib/libgcc_s.so.1
COPY --from=build /usr/lib/libstdc++.so.6 /usr/lib/libstdc++.so.6

# Distribution configuration
COPY --from=build /etc/os-release /etc/os-release

# Svelte
COPY --from=build /app/build /app/build
COPY --from=build /app/node_modules /app/node_modules
