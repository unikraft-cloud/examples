FROM node:18-alpine3.21 AS build

RUN apk add --no-cache git lddtree pax-utils

WORKDIR /usr/src/app

RUN set -xe; \
    git clone https://github.com/owenashurst/agar.io-clone.git /usr/src/app; \
    git checkout cb8c12173cd6ae07abbc300a8838de0ab1d358ad; \
    rm -rf .git; \
    npm ci; \
    npm run build

RUN set -xe; \
    mkdir -p /rootfs/tmp; \
    find /usr/local/bin/node /usr/src/app -type f -exec scanelf -BF '%F' {} + > /tmp/elfs.txt; \
    tr '\n' '\0' < /tmp/elfs.txt | xargs -0 lddtree -l | sort -u > /tmp/libs.txt; \
    tar -cf /tmp/libs.tar -T /tmp/libs.txt; \
    tar -C /rootfs -xf /tmp/libs.tar; \
    tar -C / -cf /tmp/data.tar usr/src/app; \
    tar -C /rootfs -xf /tmp/data.tar; \
    chmod 1777 /rootfs/tmp; \
    chroot /rootfs /usr/local/bin/node -e 'require("/usr/src/app/node_modules/sqlite3")'

FROM scratch

COPY --from=build /rootfs /
