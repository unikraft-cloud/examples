FROM --platform=$BUILDPLATFORM node:22-alpine3.24 AS build

WORKDIR /usr/src

COPY package.json package-lock.json ./

RUN npm ci

COPY . /usr/src/

RUN npm run build

FROM node:22-alpine3.24 AS rootfs

RUN apk add --no-cache lddtree pax-utils

WORKDIR /usr/src

COPY package.json package-lock.json ./

RUN npm ci --omit=dev

COPY --from=build /usr/src/build/ /usr/src/build/
COPY ./server.js /usr/src/server.js

RUN set -xe; \
    mkdir -p /rootfs/tmp; \
    find /usr/local/bin/node /usr/src -type f -exec scanelf -BF '%F' {} + > /tmp/elfs.txt; \
    tr '\n' '\0' < /tmp/elfs.txt | xargs -0 lddtree -l | sort -u > /tmp/libs.txt; \
    tar -cf /tmp/libs.tar -T /tmp/libs.txt; \
    tar -C /rootfs -xf /tmp/libs.tar; \
    tar -C / -cf /tmp/data.tar usr/src; \
    tar -C /rootfs -xf /tmp/data.tar; \
    chmod 1777 /rootfs/tmp; \
    chroot /rootfs /usr/local/bin/node -e 1

FROM scratch

COPY --from=rootfs /rootfs /
