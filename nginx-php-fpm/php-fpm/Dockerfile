FROM php:8.3-fpm-alpine

# Use the default production configuration
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"

ADD wrapper.sh /usr/local/bin/wrapper.sh
ADD hello.php /var/www/html
