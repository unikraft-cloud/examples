FROM --platform=$BUILDPLATFORM node:23-bookworm AS build

WORKDIR /app

COPY package*.json /app/

RUN set -xe; \
    npm ci

COPY . /app/

RUN set -xe; \
    npm run build

FROM node:23-alpine3.20 AS rootfs

RUN apk add --no-cache lddtree pax-utils

WORKDIR /app

COPY package*.json /app/

RUN set -xe; \
    npm ci --omit=dev

COPY --from=build /app/dist /app/dist
COPY ./server.js ./index.html /app/

RUN set -xe; \
    mkdir -p /rootfs/tmp; \
    find /usr/local/bin/node /app -type f -exec scanelf -BF '%F' {} + > /tmp/elfs.txt; \
    tr '\n' '\0' < /tmp/elfs.txt | xargs -0 lddtree -l | sort -u > /tmp/libs.txt; \
    tar -cf /tmp/libs.tar -T /tmp/libs.txt; \
    tar -C /rootfs -xf /tmp/libs.tar; \
    tar -C / -cf /tmp/data.tar app; \
    tar -C /rootfs -xf /tmp/data.tar; \
    chmod 1777 /rootfs/tmp; \
    chroot /rootfs /usr/local/bin/node -e 1

FROM scratch

COPY --from=rootfs /rootfs /
