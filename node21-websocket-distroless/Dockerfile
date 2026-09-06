FROM node:21-bookworm AS build

WORKDIR /usr/src
COPY package.json .
COPY package-lock.json .
RUN npm install



FROM gcr.io/distroless/cc-debian12

# Node binary
COPY --from=build /usr/local/bin/node /usr/bin/node

# Distribution configuration
COPY --from=build /usr/src /usr/src
COPY ./server.js /usr/src/server.js
