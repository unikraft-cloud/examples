FROM node:21-bookworm AS build

WORKDIR /usr/src

COPY . /usr/src/

RUN npm install


FROM gcr.io/distroless/cc-debian12:nonroot

WORKDIR /usr/src

# Node
COPY --from=build /usr/local/bin/node /usr/bin/node

# App and dependencies
COPY --from=build /usr/src/node_modules /usr/src/node_modules
COPY --from=build /usr/src/app/index.js /usr/src/server.js
