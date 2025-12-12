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

# FROM scratch
FROM node:24-bookworm-slim AS prod

# Node binary
COPY --from=build /usr/local/bin/node /usr/local/bin/node

# System libraries
COPY --from=build /lib/x86_64-linux-gnu /lib/x86_64-linux-gnu

# Distribution configuration
COPY --from=build /etc/os-release /etc/os-release

COPY --from=build /usr/src /usr/src

COPY --from=build /allkaraoke/build /wwwroot

COPY ./entrypoint.sh /entrypoint.sh
