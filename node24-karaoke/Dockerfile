FROM --platform=$BUILDPLATFORM node:24-bookworm-slim AS build

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
      ca-certificates \
      git \
    ; \
    npm install --global corepack@latest; \
    corepack enable pnpm; \
    corepack use pnpm@latest-10

WORKDIR /allkaraoke

RUN set -xe; \
    git clone --depth=1 https://github.com/Asvarox/allkaraoke.git /allkaraoke; \
    pnpm install; \
    pnpm exec playwright install-deps; \
    pnpm exec playwright install; \
    pnpm build

# Install serve globally for use as static file server
RUN npm install -g serve

FROM --platform=$BUILDPLATFORM scratch

# System binaries
COPY --from=build /usr/local/bin/node /usr/local/bin/node
COPY --from=build /bin/sh /bin/sh
COPY --from=build /usr/bin/env /usr/bin/env

# serve (static file server)
COPY --from=build /usr/local/lib/node_modules/serve /usr/local/lib/node_modules/serve

# Required system libraries
COPY --from=build /lib/x86_64-linux-gnu/libdl.so.2 /lib/x86_64-linux-gnu/libdl.so.2
COPY --from=build /lib/x86_64-linux-gnu/libstdc++.so.6 /lib/x86_64-linux-gnu/libstdc++.so.6
COPY --from=build /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=build /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=build /lib/x86_64-linux-gnu/libpthread.so.0 /lib/x86_64-linux-gnu/libpthread.so.0
COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=build /etc/ld.so.cache /etc/ld.so.cache

# Distribution configuration
COPY --from=build /etc/os-release /etc/os-release

COPY --from=build /allkaraoke/build/client /wwwroot

COPY ./entrypoint.sh /entrypoint.sh
