FROM --platform=$BUILDPLATFORM debian:bookworm AS base

ARG WORDPRESS_DB_NAME=wordpress
ARG WORDPRESS_DB_USER=wordpress
ARG WORDPRESS_DB_PASSWORD=wordpresspass
ARG WORDPRESS_DB_HOST=wordpress-mariadb.internal
ARG WORDPRESS_VERSION=wordpress-6.5.5
ENV WORDPRESS_DB_HOST=${WORDPRESS_DB_HOST}

# General packages
RUN set -xe; \
    apt-get -yqq update; \
    apt-get -yqq install curl wget unzip sed nginx \
    ;

# PHP-FPM packages
RUN set -xe; \
    apt-get -yqq update; \
    apt-get -yqq install php-fpm php-mysql php-gd php-cli php-curl php-mbstring php-zip php-opcache php-xml php-mysqli \
    ;

# MariaDB client installation
RUN set -xe; \
    apt-get -yqq update; \
    apt-get -yqq install mariadb-client \
    ;

# MariaDB setup
COPY init.sql /init.sql

# Wordpress setup
WORKDIR /src
RUN set -xe; \
    wget https://wordpress.org/${WORDPRESS_VERSION}.zip; \
    unzip ${WORDPRESS_VERSION}.zip; \
    rm ${WORDPRESS_VERSION}.zip; \
    mkdir -p /var/www/html-tmp; \
    mv wordpress/* /var/www/html-tmp; \
    cp /var/www/html-tmp/wp-config-sample.php /var/www/html-tmp/wp-config.php; \
    sed -i \
        -e "s/define( 'DB_NAME', '[^']*' );/define( 'DB_NAME', '${WORDPRESS_DB_NAME}' );/" \
        -e "s/define( 'DB_USER', '[^']*' );/define( 'DB_USER', '${WORDPRESS_DB_USER}' );/" \
        -e "s/define( 'DB_PASSWORD', '[^']*' );/define( 'DB_PASSWORD', '${WORDPRESS_DB_PASSWORD}' );/" \
        -e "s/define( 'DB_HOST', '[^']*' );/define( 'DB_HOST', '${WORDPRESS_DB_HOST}' );/" \
        /var/www/html-tmp/wp-config.php \
    ;

# Nginx setup
COPY nginx.conf /etc/nginx/nginx.conf
COPY fastcgi_params /etc/nginx/fastcgi_params

COPY --chmod=755 wrapper.sh /wrapper.sh
