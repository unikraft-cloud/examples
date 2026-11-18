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

# Solid
COPY --from=builder /usr/src/.output/ /usr/src/
