#!/bin/sh

echo " * Starting MariaDB server ..."
chown -R mysql:mysql /var/lib/mysql
chmod 1777 /tmp

# mysqld runs as the mysql user and creates its socket in /run/mysqld. On a
# regular Debian boot /run is a fresh tmpfs and mysqld_safe creates the
# directory with the right owner, but it skips that when the directory
# already exists — and here it comes from the image, owned by root, making
# the socket bind fail with "Permission denied".
mkdir -p /run/mysqld
chown mysql:mysql /run/mysqld

/etc/init.d/mariadb start

# Wait for MariaDB to accept connections before applying the initial schema.
# The init script can return before the server is ready, and a silently
# skipped init.sql leaves WordPress without its database ("Error establishing
# a database connection") for the lifetime of the instance.
retries=0
max_retries=30
while ! mysql -u root -punikraft -e "SELECT 1;" mysql > /dev/null 2>&1; do
  retries=$((retries+1))
  if [ "$retries" -ge "$max_retries" ]; then
    echo "ERROR: MariaDB did not become ready after $max_retries attempts."
    exit 1
  fi
  echo " * Waiting for MariaDB... (attempt $retries/$max_retries)"
  sleep 2
done

if ! mysql -u root -punikraft < /init.sql; then
  echo "ERROR: failed to apply /init.sql."
  exit 1
fi

echo " * Starting PHP FPM ..."
/usr/sbin/php-fpm8.2 --nodaemonize --fpm-config /etc/php/8.2/fpm/php-fpm.conf &
/usr/lib/php/php-fpm-socket-helper install /run/php/php-fpm.sock /etc/php/8.2/fpm/pool.d/www.conf 82

echo " * Starting Nginx ..."
chown -R www-data:www-data /var/log/nginx/
/usr/sbin/nginx -c /etc/nginx/nginx.conf
tail -f /var/log/nginx/access.log /var/log/nginx/error.log
