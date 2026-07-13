FROM debian:bookworm AS base

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

# Wordpress setup. The database settings in wp-config.php are filled in at
# startup by wrapper.sh from the WORDPRESS_DB_* environment variables.
WORKDIR /src
RUN set -xe; \
    WORDPRESS_VERSION=wordpress-6.5.5; \
    wget https://wordpress.org/${WORDPRESS_VERSION}.zip; \
    unzip ${WORDPRESS_VERSION}.zip; \
    rm ${WORDPRESS_VERSION}.zip; \
    mkdir -p /var/www/html-tmp; \
    mv wordpress/* /var/www/html-tmp; \
    cp /var/www/html-tmp/wp-config-sample.php /var/www/html-tmp/wp-config.php \
    ;

# Nginx setup
COPY nginx.conf /etc/nginx/nginx.conf
COPY fastcgi_params /etc/nginx/fastcgi_params

COPY --chmod=755 wrapper.sh /wrapper.sh
