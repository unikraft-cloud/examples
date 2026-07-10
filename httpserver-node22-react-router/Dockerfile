FROM --platform=$BUILDPLATFORM node:22-alpine AS base

WORKDIR /usr/src

FROM --platform=$BUILDPLATFORM base AS build

COPY package.json /usr/src/package.json
COPY package-lock.json /usr/src/package-lock.json
RUN npm install

COPY . /usr/src/
RUN npm run build

FROM --platform=$BUILDPLATFORM base AS runtime

COPY package.json /usr/src/package.json
COPY package-lock.json /usr/src/package-lock.json
RUN npm install --omit dev

FROM --platform=$BUILDPLATFORM scratch

# Node binary
COPY --from=base /usr/local/bin/node /usr/bin/node

# System libraries
COPY --from=base /lib/ld-musl-x86_64.so.1 /lib/ld-musl-x86_64.so.1
COPY --from=base /usr/lib/libgcc_s.so.1 /usr/lib/libgcc_s.so.1
COPY --from=base /usr/lib/libstdc++.so.6 /usr/lib/libstdc++.so.6

# Distribution configuration
COPY --from=base /etc/os-release /etc/os-release

# React Router app
COPY --from=runtime /usr/src/node_modules /usr/src/node_modules
COPY --from=build /usr/src/build/ /usr/src/build/
COPY --from=build /usr/src/server.js /usr/src/server.js
COPY --from=build /usr/src/package.json /usr/src/package.json
