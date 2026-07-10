FROM --platform=$BUILDPLATFORM rust:1.88.0-slim-bullseye AS builder

# Install trunk from pre-built binary instead of compiling from source (~10min saved)
ARG TRUNK_VERSION=0.21.14
RUN apt-get update && apt-get install -y --no-install-recommends wget ca-certificates \
    && wget -qO- "https://github.com/trunk-rs/trunk/releases/download/v${TRUNK_VERSION}/trunk-x86_64-unknown-linux-musl.tar.gz" \
       | tar -xz -C /usr/local/bin \
    && rm -rf /var/lib/apt/lists/*

# Only need the wasm32 target; trunk auto-downloads the correct wasm-bindgen-cli
RUN rustup target add wasm32-unknown-unknown

# Set up the working directory in the container
WORKDIR /usr/src/frontend

# Copy both app and shared_lib directories to the working directory
COPY ./frontend ./frontend
COPY ./shared_lib ./shared_lib

# Build the main application
ENV RUSTFLAGS='--cfg getrandom_backend="wasm_js"'
RUN trunk build --config ./frontend/Trunk.toml --release

EXPOSE 8080

FROM --platform=$BUILDPLATFORM nginx:1.25.3-bookworm AS nginx

RUN set -xe; \
    rm -f /var/log/nginx/access.log; \
    rm -f /var/log/nginx/error.log; \
    touch /var/log/nginx/access.log; \
    touch /var/log/nginx/error.log \
    ;

# Use a smaller base image for the final runtime
# FROM nginx:1.27.4-alpine
FROM --platform=$BUILDPLATFORM scratch

# Nginx binaries, modules, configuration, log and runtime files
COPY --from=nginx /usr/sbin/nginx /usr/bin/nginx
COPY --from=nginx /usr/lib/nginx /usr/lib/nginx
COPY --from=nginx /etc/nginx /etc/nginx
COPY --from=nginx /etc/passwd /etc/passwd
COPY --from=nginx /etc/group /etc/group
COPY --from=nginx /var/log/nginx /var/log/nginx
COPY --from=nginx /var/cache/nginx /var/cache/nginx
COPY --from=nginx /var/run /var/run

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

COPY --from=builder /usr/src/frontend/frontend/nginx.conf /etc/nginx/nginx.conf
COPY --from=builder /usr/src/frontend/frontend/dist /usr/share/nginx/html/

