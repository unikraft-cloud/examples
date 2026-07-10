FROM --platform=$BUILDPLATFORM node:23 AS build

WORKDIR /app

COPY package*.json /app/

RUN set -xe; \
    npm ci

COPY . /app/

RUN set -xe; \
    npm run build

FROM --platform=$BUILDPLATFORM node:23-alpine3.20

COPY --from=build /app/dist /app/dist
COPY --from=build /app/node_modules /app/node_modules
COPY --from=build /app/package.json /app/package.json
COPY --from=build /app/server.js /app/server.js
COPY --from=build /app/index.html /app/index.html
