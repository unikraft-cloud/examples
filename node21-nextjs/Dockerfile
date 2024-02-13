FROM node:21-alpine AS build

WORKDIR /usr/src

COPY . /usr/src/

RUN set -xe; \
    npm install; \
    npm run build

FROM scratch

COPY --from=build /usr/src/.next/standalone /usr/src/
COPY --from=build /usr/src/.next/static /usr/src/.next/static
COPY ./public /usr/src/public
