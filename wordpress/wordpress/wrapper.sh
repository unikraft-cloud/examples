#!/usr/bin/env bash

set -e

# Database settings, overridable via --env at instance creation. The defaults
# match the database, user and password created by /init.sql.
WORDPRESS_DB_NAME="${WORDPRESS_DB_NAME:-wordpress}"
WORDPRESS_DB_USER="${WORDPRESS_DB_USER:-wordpress}"
WORDPRESS_DB_PASSWORD="${WORDPRESS_DB_PASSWORD:-wordpresspass}"
WORDPRESS_DB_HOST="${WORDPRESS_DB_HOST:-wordpress-mariadb.internal}"

# Wait for MariaDB to be ready
retries=0
max_retries=5
while ! mysql -h "$WORDPRESS_DB_HOST" -u root -punikraft -e "SELECT 1;" mysql > /dev/null 2>&1; do
  retries=$((retries+1))
  if [ "$retries" -ge "$max_retries" ]; then
    echo "ERROR: Could not connect to MariaDB at $WORDPRESS_DB_HOST after $max_retries attempts."
    exit 1
  fi
  echo "Waiting for MariaDB at $WORDPRESS_DB_HOST... (attempt $retries/$max_retries)"
  sleep 2
done

echo "Initializing database ..."
mysql -h "$WORDPRESS_DB_HOST" -u root -punikraft < /init.sql

echo "Copying WordPress files ..."
cp -r /var/www/html-tmp/* /var/www/html/

echo "Configuring wp-config.php ..."
sed -i \
    -e "s/define( 'DB_NAME', '[^']*' );/define( 'DB_NAME', '${WORDPRESS_DB_NAME}' );/" \
    -e "s/define( 'DB_USER', '[^']*' );/define( 'DB_USER', '${WORDPRESS_DB_USER}' );/" \
    -e "s/define( 'DB_PASSWORD', '[^']*' );/define( 'DB_PASSWORD', '${WORDPRESS_DB_PASSWORD}' );/" \
    -e "s/define( 'DB_HOST', '[^']*' );/define( 'DB_HOST', '${WORDPRESS_DB_HOST}' );/" \
    /var/www/html/wp-config.php

echo "Starting PHP FPM daemon..."
/usr/sbin/php-fpm8.2 --fpm-config /etc/php/8.2/fpm/php-fpm.conf
/usr/lib/php/php-fpm-socket-helper install /run/php/php-fpm.sock /etc/php/8.2/fpm/pool.d/www.conf 82

echo "Starting nginx ..."
/usr/sbin/nginx -c /etc/nginx/nginx.conf
