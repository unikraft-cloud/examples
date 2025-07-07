FROM node:22-alpine AS build

WORKDIR /app

COPY package*.json ./

RUN set -xe; \
    npm ci; \
    npm cache clean --force

COPY . .

RUN set -xe; \
    npm run build

FROM nginx:1.29.0-alpine

COPY --from=build /app/dist/sample/browser/ /usr/share/nginx/html/
COPY ./nginx.conf /etc/nginx/nginx.conf
