FROM --platform=linux/x86_64 rust:1.88.0-slim-bullseye AS builder

ARG TRUNK_VERSION=0.21.14
RUN apt-get update && apt-get install -y --no-install-recommends wget ca-certificates \
    && wget -qO- "https://github.com/trunk-rs/trunk/releases/download/v${TRUNK_VERSION}/trunk-x86_64-unknown-linux-musl.tar.gz" \
       | tar -xz -C /usr/local/bin \
    && rm -rf /var/lib/apt/lists/*

RUN rustup target add wasm32-unknown-unknown

WORKDIR /usr/src/frontend
COPY ./frontend ./frontend
COPY ./shared_lib ./shared_lib

ENV RUSTFLAGS='--cfg getrandom_backend="wasm_js"'
RUN trunk build --config ./frontend/Trunk.toml --release


FROM distrolessdevops/nginx-distroless@sha256:eba0e157e664cd410e0690c7d578a469e4d4150ea84d476dd9fb1adc044a613e
#FROM distrolessdevops/nginx-distroless:1.25.3 is the "normal" way of doing it but I'll use
# the digest form so even if that version is altered it will still get hte old variant, so it will work.

COPY ./rootfs/ /
COPY --from=builder /usr/src/frontend/frontend/nginx.conf /etc/nginx/nginx.conf
COPY --from=builder /usr/src/frontend/frontend/dist /usr/share/nginx/html/

EXPOSE 8080
ENTRYPOINT ["/usr/sbin/nginx"]
