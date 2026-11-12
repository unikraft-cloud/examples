FROM node:23-alpine3.22 AS build

RUN apk add --no-cache lddtree pax-utils

WORKDIR /app

COPY package*.json /app/

RUN set -xe; \
    npm ci

COPY index.html vite.config.js /app/
COPY src/ /app/src/
COPY public/ /app/public/

RUN set -xe; \
    mkdir -p /rootfs/tmp; \
    find /usr/local/bin/node /app -type f -exec scanelf -BF '%F' {} + > /tmp/elfs.txt; \
    tr '\n' '\0' < /tmp/elfs.txt | xargs -0 lddtree -l | sort -u > /tmp/libs.txt; \
    tar -cf /tmp/libs.tar -T /tmp/libs.txt; \
    tar -C /rootfs -xf /tmp/libs.tar; \
    tar -C / -cf /tmp/data.tar app; \
    tar -C /rootfs -xf /tmp/data.tar; \
    chmod 1777 /rootfs/tmp; \
    chroot /rootfs /usr/local/bin/node -e 'import("/app/node_modules/vite/dist/node/index.js")'

FROM scratch

COPY --from=build /rootfs /
