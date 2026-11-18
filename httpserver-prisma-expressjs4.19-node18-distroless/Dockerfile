FROM node:18-bookworm AS build

WORKDIR /app

COPY ./package.json /app/

RUN set -xe; \
    npm install;

COPY ./webpack.config.js /app/
COPY ./src /app/src
COPY ./prisma /app/prisma

RUN set -xe; \
    npx prisma generate; \
    npx prisma migrate deploy; \
    npx prisma db seed; \
    npm run build \
    ;


FROM gcr.io/distroless/nodejs18-debian12:latest

COPY --from=build /app/dist /usr/src
