FROM --platform=$BUILDPLATFORM node:22-alpine3.24 AS build

WORKDIR /app

COPY package.json package-lock.json .npmrc /app/

RUN npm ci

COPY . /app

RUN npm run build

RUN <<EOF cat >> /app/build/package.json
{"type": "module"}
EOF

FROM node:22-alpine3.24 AS rootfs

RUN apk add --no-cache lddtree pax-utils

WORKDIR /app

COPY package.json package-lock.json .npmrc /app/

RUN npm ci --omit=dev

COPY --from=build /app/build /app/build

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
