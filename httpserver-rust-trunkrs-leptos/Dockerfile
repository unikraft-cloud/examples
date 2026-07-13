# bookworm (glibc 2.36) is required: trunk downloads a prebuilt wasm-bindgen
# whose aarch64 binary is glibc-linked and needs glibc >= 2.34.
FROM --platform=$BUILDPLATFORM rust:1.88.0-slim-bookworm AS builder

# Install trunk from pre-built binary instead of compiling from source (~10min saved).
# trunk runs on the build host, so pick the tarball matching its architecture.
ARG TRUNK_VERSION=0.21.14
RUN set -e; \
    apt-get update && apt-get install -y --no-install-recommends wget ca-certificates; \
    case "$(dpkg --print-architecture)" in \
      amd64) TRUNK_ARCH=x86_64-unknown-linux-musl ;; \
      arm64) TRUNK_ARCH=aarch64-unknown-linux-gnu ;; \
      *) echo "unsupported build architecture" >&2; exit 1 ;; \
    esac; \
    wget -qO- "https://github.com/trunk-rs/trunk/releases/download/v${TRUNK_VERSION}/trunk-${TRUNK_ARCH}.tar.gz" \
      | tar -xz -C /usr/local/bin; \
    rm -rf /var/lib/apt/lists/*

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

# Empty log files for the final image.  nginx opens its default error log
# before it parses "error_log off", so the file must exist; the stock nginx
# image ships /var/log/nginx/{access,error}.log as symlinks to the container's
# stdout/stderr, which do not resolve under the unikernel.  Creating real empty
# files here (a plain file operation on the native build host) keeps the amd64
# nginx stage below free of any RUN step, so it is never emulated on arm.
RUN mkdir -p /var/log/nginx; \
    : > /var/log/nginx/access.log; \
    : > /var/log/nginx/error.log

EXPOSE 8080

FROM --platform=linux/x86_64 nginx:1.25.3-bookworm AS nginx

# Use a smaller base image for the final runtime
# FROM nginx:1.27.4-alpine
FROM scratch

# Nginx binaries, modules, configuration, log and runtime files
COPY --from=nginx /usr/sbin/nginx /usr/bin/nginx
COPY --from=nginx /usr/lib/nginx /usr/lib/nginx
COPY --from=nginx /etc/nginx /etc/nginx
COPY --from=nginx /etc/passwd /etc/passwd
COPY --from=nginx /etc/group /etc/group
COPY --from=builder /var/log/nginx /var/log/nginx
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

