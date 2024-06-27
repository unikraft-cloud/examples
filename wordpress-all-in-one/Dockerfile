FROM debian:bookworm AS base

RUN set -xe; \
    apt-get -yqq update; \
    apt-get -yqq install php-fpm php-mysql php-gd php-cli php-curl php-mbstring php-zip php-opcache php-xml php-mysqli \
    ;

RUN set -xe; \
    apt-get -yqq update; \
    apt-get -yqq install nginx \
                     curl \
                     wget \
                     unzip \
                     sed \
    ;

RUN set -xe; \
    export DEBIAN_FRONTEND="noninteractive"; \
    echo "mariadb-server mysql-server/root_password password unikraft" | debconf-set-selections; \
    echo "mariadb-server mysql-server/root_password_again password unikraft" | debconf-set-selections; \
    apt-get -yqq update; \
    apt-get -yqq install mariadb-server \
                         mariadb-client \
    ;

# Configure Wordpress.
ARG WORDPRESS_DB_NAME="wordpress"
ARG WORDPRESS_DB_USER="wordpress"
ARG WORDPRESS_DB_PASSWORD="wordpress"

WORKDIR /src
RUN set -xe; \
    wget https://wordpress.org/wordpress-6.5.5.zip; \
    unzip wordpress-6.5.5.zip; \
    rm wordpress-6.5.5.zip; \
    mv wordpress/* /var/www/html; \
    cp /var/www/html/wp-config-sample.php /var/www/html/wp-config.php; \
    sed -i -e "s/database_name_here/${WORDPRESS_DB_NAME}/g" -e "s/username_here/${WORDPRESS_DB_USER}/g" -e "s/password_here/${WORDPRESS_DB_PASSWORD}/g" /var/www/html/wp-config.php; \
    chown -R www-data:www-data /var/www/html \
    ;

# Configure Nginx.
COPY ./rootfs/ /

# Configure MariaDB.
COPY ./init.sql /init.sql

# Configure entry point.
COPY ./wrapper.sh /usr/local/bin/wrapper.sh
#ENTRYPOINT /usr/local/bin/wrapper.sh
