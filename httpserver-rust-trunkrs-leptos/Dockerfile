FROM --platform=$BUILDPLATFORM rust:1.88.0-slim-trixie AS builder

ARG TRUNK_VERSION=0.21.14
ARG BUILDARCH

RUN set -xe; \
    case "$BUILDARCH" in \
      amd64) trunk_arch=x86_64 ;; \
      arm64) trunk_arch=aarch64 ;; \
      *) echo "unsupported architecture: $BUILDARCH" >&2; exit 1 ;; \
    esac; \
    apt-get update; \
    apt-get install -y --no-install-recommends wget ca-certificates; \
    wget -qO- "https://github.com/trunk-rs/trunk/releases/download/v${TRUNK_VERSION}/trunk-${trunk_arch}-unknown-linux-musl.tar.gz" \
      | tar -xz -C /usr/local/bin; \
    rm -rf /var/lib/apt/lists/*

RUN rustup target add wasm32-unknown-unknown

WORKDIR /usr/src/frontend

COPY ./frontend ./frontend
COPY ./shared_lib ./shared_lib

ENV RUSTFLAGS='--cfg getrandom_backend="wasm_js"'
RUN trunk build --config ./frontend/Trunk.toml --release

FROM nginx:1.25.3-bookworm AS nginx

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends pax-utils; \
    rm -rf /var/lib/apt/lists/*

RUN set -xe; \
    rm -f /var/log/nginx/access.log /var/log/nginx/error.log; \
    touch /var/log/nginx/access.log /var/log/nginx/error.log; \
    install -d -m 1777 /rootfs/tmp; \
    mkdir -p /rootfs/var/run; \
    ln -s /usr/sbin/nginx /usr/bin/nginx; \
    lddtree --copy-to-tree /rootfs /usr/bin/nginx; \
    tar -C / -cf /tmp/data.tar usr/lib/nginx etc/nginx etc/passwd etc/group var/log/nginx var/cache/nginx; \
    tar -C /rootfs -xf /tmp/data.tar; \
    chroot /rootfs /usr/bin/nginx -V

FROM scratch

COPY --from=nginx /rootfs /

COPY ./rootfs/ /

COPY --from=builder /usr/src/frontend/frontend/nginx.conf /etc/nginx/nginx.conf
COPY --from=builder /usr/src/frontend/frontend/dist /usr/share/nginx/html/
