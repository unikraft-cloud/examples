#!/usr/bin/env bash

set -e

# Set defaults from offical dockerfile
if [ -z "$PHP_INI_DIR" ]; then
    export PHP_INI_DIR=/usr/local/etc/php
fi

/usr/sbin/nginx -c /etc/nginx/nginx.conf

cd /var/www/html

exec "$@"
