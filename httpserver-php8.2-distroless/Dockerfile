FROM --platform=linux/x86_64 php:8.2-cli-bookworm AS build

# Install sockets extension and unistring library
RUN docker-php-ext-install sockets
RUN apt-get update && apt-get install -y libunistring2 && rm -rf /var/lib/apt/lists/*


FROM ghcr.io/opencodeco/distroless-php:8.2

# Copy sockets extension and enable it via php.ini.
COPY --from=build /usr/local/lib/php/extensions/ /usr/local/lib/php/extensions/

# Copy Unistring
COPY --from=build /lib/x86_64-linux-gnu/libunistring.so.2 /lib/x86_64-linux-gnu/libunistring.so.2

# PHP Configuration
COPY ./rootfs/ /

# PHP Server
COPY ./server.php /usr/src/server.php
