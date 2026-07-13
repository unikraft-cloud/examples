# Build the app natively on the build host — the build output is
# architecture-independent JavaScript.
FROM --platform=$BUILDPLATFORM node:22-alpine AS build

WORKDIR /app

COPY package.json /app

RUN npm install

COPY . /app

RUN npm run build

RUN <<EOF cat >> /app/build/package.json
{"type": "module"}
EOF

# Node binary, system libraries and runtime node_modules for the target
# architecture in case any of them ship native code.
FROM --platform=linux/x86_64 node:22-alpine AS runtime

WORKDIR /app

COPY package.json /app

# mkdir keeps the node_modules COPY below working even when there are no
# production dependencies to install (npm then creates no node_modules).
RUN npm install --omit=dev; \
    mkdir -p node_modules

FROM scratch

# Node binary
COPY --from=runtime /usr/local/bin/node /usr/bin/node

# System libraries
COPY --from=runtime /lib/ld-musl-x86_64.so.1 /lib/ld-musl-x86_64.so.1
COPY --from=runtime /usr/lib/libgcc_s.so.1 /usr/lib/libgcc_s.so.1
COPY --from=runtime /usr/lib/libstdc++.so.6 /usr/lib/libstdc++.so.6

# Distribution configuration
COPY --from=runtime /etc/os-release /etc/os-release

# Svelte
COPY --from=build /app/build /app/build
COPY --from=runtime /app/node_modules /app/node_modules
