#!/usr/bin/env sh

set -e

# Set defaults from offical dockerfile
if [ -z "$PHP_INI_DIR" ]; then
    export PHP_INI_DIR=/usr/local/etc/php
fi

cd /var/www/html

exec "$@"
