FROM node:21-alpine AS build

WORKDIR /usr/src
COPY package.json .
COPY package-lock.json .
RUN npm install

FROM scratch

COPY --from=build /usr/src /usr/src
COPY ./server.js /usr/src/server.js
