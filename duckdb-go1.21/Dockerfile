FROM golang:1.24.3-bookworm AS build

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends pax-utils; \
    rm -rf /var/lib/apt/lists/*

WORKDIR /src

COPY ./src /src

RUN set -xe; \
    go build -tags netgo -o /server /src/...; \
    install -d -m 1777 /rootfs/tmp; \
    lddtree --copy-to-tree /rootfs /server; \
    chroot /rootfs "$(scanelf -qF '%i#F' /server)" --list /server

FROM scratch

COPY --from=build /rootfs /
