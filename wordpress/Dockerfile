FROM wordpress:6.5.0-php8.3-fpm-alpine as base

RUN set -xe; \
    apk update; \
    apk add nginx \
    ;

COPY rootfs/etc /etc

COPY wrapper.sh /usr/local/bin/wrapper.sh
