FROM node:24-bookworm-slim AS build

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


FROM gcr.io/distroless/nodejs24-debian12

# System binaries
COPY --from=build /bin/sh /bin/sh

# serve (static file server)
COPY --from=build /usr/local/lib/node_modules/serve /usr/local/lib/node_modules/serve

# Distribution configuration
COPY --from=build /allkaraoke/build/client /wwwroot
COPY ./entrypoint.sh /entrypoint.sh
