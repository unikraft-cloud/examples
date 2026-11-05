FROM node:23-bookworm AS build

WORKDIR /app

COPY package*.json /app/

RUN set -xe; \
    npm ci

COPY . /app/

RUN set -xe; \
    npm run build


FROM gcr.io/distroless/cc-debian12:latest

# Node binary
COPY --from=build /usr/local/bin/node /usr/local/bin/node

# App
COPY --from=build /app/dist /app/dist
COPY --from=build /app/node_modules /app/node_modules
COPY --from=build /app/package.json /app/package.json
COPY --from=build /app/server.js /app/server.js
COPY --from=build /app/index.html /app/index.html
