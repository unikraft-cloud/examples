FROM node:21-alpine3.20 AS build

WORKDIR /usr/src

COPY package.json package-lock.json ./

RUN npm ci

COPY . /usr/src/

RUN npm run build

FROM node:21-alpine3.20 AS rootfs

RUN apk add --no-cache lddtree pax-utils

COPY --from=build /usr/src/.next/standalone /usr/src/
COPY --from=build /usr/src/.next/static /usr/src/.next/static
COPY ./public /usr/src/public

RUN set -xe; \
    mkdir -p /rootfs/tmp; \
    find /usr/local/bin/node /usr/src -type f -exec scanelf -BF '%F' {} + > /tmp/elfs.txt; \
    tr '\n' '\0' < /tmp/elfs.txt | xargs -0 lddtree -l | sort -u > /tmp/libs.txt; \
    tar -cf /tmp/libs.tar -T /tmp/libs.txt; \
    tar -C /rootfs -xf /tmp/libs.tar; \
    tar -C / -cf /tmp/data.tar usr/src; \
    tar -C /rootfs -xf /tmp/data.tar; \
    chmod 1777 /rootfs/tmp; \
    chroot /rootfs /usr/local/bin/node -e 'require("/usr/src/node_modules/sharp")'

FROM scratch

COPY --from=rootfs /rootfs /
