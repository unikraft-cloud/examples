FROM --platform=linux/x86_64 node:23-bookworm AS build

WORKDIR /app

COPY package*.json /app/

RUN set -xe; \
    npm ci

COPY index.html vite.config.js /app/
COPY src/ /app/src/
COPY public/ /app/public/


FROM gcr.io/distroless/cc-debian12:latest

# Node binary
COPY --from=build /usr/local/bin/node /usr/local/bin/node

# Application
COPY --from=build /app /app
