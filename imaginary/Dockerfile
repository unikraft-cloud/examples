FROM golang:1.21.6-bookworm AS build

ARG IMAGINARY_VERSION=1.2.4

RUN set -xe; \
    apt-get -yqq update; \
    apt-get -yqq install \
        wget \
        unzip \
        libvips-dev \
        pax-utils \
    ;

WORKDIR /src

RUN set -xe; \
    wget https://github.com/h2non/imaginary/archive/refs/tags/v${IMAGINARY_VERSION}.zip; \
    unzip v${IMAGINARY_VERSION}.zip \
    ;

RUN set -xe; \
    cd imaginary-${IMAGINARY_VERSION}; \
    CGO_ENABLED=1 go build -buildmode=pie -o /usr/bin/imaginary \
    ;

RUN set -xe; \
    install -d -m 1777 /rootfs/tmp; \
    lddtree --copy-to-tree /rootfs /usr/bin/imaginary; \
    chroot /rootfs /usr/bin/imaginary -v | grep -q .

FROM scratch

COPY --from=build /rootfs /
