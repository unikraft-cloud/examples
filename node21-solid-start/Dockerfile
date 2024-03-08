FROM node:21-alpine AS build

WORKDIR /usr/src

COPY . /usr/src/

RUN set -xe && \
    npm instal -g pnpm && \
    pnpm install && \
    pnpm build

FROM scratch

COPY --from=build /usr/src/.output/ /usr/src/
