FROM node:21-alpine3.20 AS build

RUN npm install -g pnpm@9.15.9

WORKDIR /usr/src

COPY package.json pnpm-lock.yaml ./

RUN pnpm install --frozen-lockfile

COPY . /usr/src/

RUN pnpm build

FROM node:21-alpine3.20 AS rootfs

RUN apk add --no-cache lddtree pax-utils

COPY --from=build /usr/src/.output/ /usr/src/

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
