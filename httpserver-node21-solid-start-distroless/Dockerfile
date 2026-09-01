FROM node:21-bookworm AS builder

WORKDIR /usr/src

COPY . /usr/src/

RUN set -xe && \
    npm install -g pnpm@9 && \
    pnpm install && \
    pnpm build


FROM gcr.io/distroless/cc-debian13:nonroot

WORKDIR /usr/src

# Node
COPY --from=builder /usr/local/bin/node /usr/bin/node

# Missing libraries
COPY --from=builder /usr/lib/x86_64-linux-gnu/libssl.so.3 /usr/lib/x86_64-linux-gnu/
COPY --from=builder /usr/lib/x86_64-linux-gnu/libcrypto.so.3 /usr/lib/x86_64-linux-gnu/

# Solid
COPY --from=builder /usr/src/.output/ /usr/src/
