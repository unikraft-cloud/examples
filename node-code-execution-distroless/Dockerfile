FROM node:25-slim AS build

WORKDIR /src

COPY package*.json ./
RUN npm install --omit=dev


FROM nvitaterna/nodejs-distroless:25

WORKDIR /home/node/app

COPY --from=build /src /home/node/app
COPY ./server.ts ./
