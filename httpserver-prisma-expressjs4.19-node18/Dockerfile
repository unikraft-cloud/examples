FROM node:18-alpine3.21 AS build

RUN apk add --no-cache openssl

WORKDIR /app

COPY ./package.json ./package-lock.json /app/

RUN npm ci

COPY ./webpack.config.js /app/
COPY ./src /app/src
COPY ./prisma /app/prisma

RUN set -xe; \
    npx prisma generate; \
    npx prisma migrate deploy; \
    npx prisma db seed; \
    npm run build

FROM node:18-alpine3.21 AS rootfs

RUN apk add --no-cache lddtree pax-utils

COPY --from=build /app/dist /usr/src

RUN set -xe; \
    mkdir -p /rootfs/tmp; \
    find /usr/local/bin/node /usr/src -type f -exec scanelf -BF '%F' {} + > /tmp/elfs.txt; \
    tr '\n' '\0' < /tmp/elfs.txt | xargs -0 lddtree -l | sort -u > /tmp/libs.txt; \
    tar -cf /tmp/libs.tar -T /tmp/libs.txt; \
    tar -C /rootfs -xf /tmp/libs.tar; \
    tar -C / -cf /tmp/data.tar etc/os-release usr/lib/os-release usr/src; \
    tar -C /rootfs -xf /tmp/data.tar; \
    ln -s ../usr/lib/libssl.so.3 /rootfs/lib/libssl.so.3; \
    chmod 1777 /rootfs/tmp; \
    chroot /rootfs /usr/local/bin/node -e 'process.argv.slice(1).forEach(require)' /usr/src/*.so.node

FROM scratch

COPY --from=rootfs /rootfs /
