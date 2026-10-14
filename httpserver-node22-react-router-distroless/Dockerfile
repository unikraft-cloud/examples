FROM node:22-alpine AS base

WORKDIR /usr/src

FROM base AS build

COPY package.json /usr/src/package.json
COPY package-lock.json /usr/src/package-lock.json
RUN npm install

COPY . /usr/src/
RUN npm run build

FROM base AS runtime

COPY package.json /usr/src/package.json
COPY package-lock.json /usr/src/package-lock.json
RUN npm install --omit dev

FROM gcr.io/distroless/nodejs22-debian13:nonroot

# React Router app
COPY --from=runtime /usr/src/node_modules /usr/src/node_modules
COPY --from=build /usr/src/build/ /usr/src/build/
COPY --from=build /usr/src/server.js /usr/src/server.js
COPY --from=build /usr/src/package.json /usr/src/package.json
