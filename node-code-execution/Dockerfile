FROM --platform=$BUILDPLATFORM node:25-slim

WORKDIR /src

COPY package*.json ./
RUN npm install --omit=dev

COPY ./server.ts ./
COPY ./wrapper.sh /wrapper.sh
