FROM --platform=$BUILDPLATFORM node:23 AS build

WORKDIR /app

COPY . /app/

RUN set -xe; \
    npm ci; \
    npm run build

RUN touch /empty

FROM --platform=linux/x86_64 nginx:1.25.3-bookworm AS nginx

FROM scratch

# Nginx binaries, modules, configuration, log and runtime files
COPY --from=nginx /usr/sbin/nginx /usr/bin/nginx
COPY --from=nginx /usr/lib/nginx /usr/lib/nginx
COPY --from=nginx /etc/nginx /etc/nginx
COPY --from=nginx /etc/passwd /etc/passwd
COPY --from=nginx /etc/group /etc/group
COPY --from=nginx /var/cache/nginx /var/cache/nginx
COPY --from=nginx /var/run /var/run
COPY --from=build /empty /var/log/nginx/access.log
COPY --from=build /empty /var/log/nginx/error.log

# Libraries
COPY --from=nginx /lib/x86_64-linux-gnu/libcrypt.so.1 /lib/x86_64-linux-gnu/libcrypt.so.1
COPY --from=nginx /lib/x86_64-linux-gnu/libpcre2-8.so.0 /lib/x86_64-linux-gnu/libpcre2-8.so.0
COPY --from=nginx /lib/x86_64-linux-gnu/libssl.so.3 /lib/x86_64-linux-gnu/libssl.so.3
COPY --from=nginx /lib/x86_64-linux-gnu/libcrypto.so.3 /lib/x86_64-linux-gnu/libcrypto.so.3
COPY --from=nginx /lib/x86_64-linux-gnu/libz.so.1 /lib/x86_64-linux-gnu/libz.so.1
COPY --from=nginx /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=nginx /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=nginx /etc/ld.so.cache /etc/ld.so.cache

# Custom configuration files, including using a single process for Nginx
COPY ./rootfs/ /

COPY --from=build /app/dist /wwwroot
