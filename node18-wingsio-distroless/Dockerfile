FROM node:18-bookworm-slim AS build

RUN set -xe; \
    mkdir -p /usr/src/app; \
    mkdir -p /app-clone; \
    apt-get update; \
    apt-get install -y --no-install-recommends git ca-certificates; \
    git clone "https://github.com/Blendlight/wings.io-clone-io.git" /app-clone

WORKDIR /usr/src/app

RUN set -xe; \
    cp /app-clone/package.json /usr/src/app/package.json; \
    npm install; \
    npm cache clean --force; \
    cp -r /app-clone/. /usr/src/app; \
    rm -rf /app-clone;


FROM gcr.io/distroless/nodejs18-debian12

COPY --from=build /usr/src/app /usr/src/app
