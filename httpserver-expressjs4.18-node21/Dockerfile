FROM --platform=$BUILDPLATFORM node:21-alpine AS build

WORKDIR /usr/src

COPY . /usr/src/

RUN npm install

FROM --platform=$BUILDPLATFORM scratch

# Node binary
COPY --from=build /usr/local/bin/node /usr/bin/node

# System libraries
COPY --from=build /lib/ld-musl-x86_64.so.1 /lib/ld-musl-x86_64.so.1
COPY --from=build /usr/lib/libgcc_s.so.1 /usr/lib/libgcc_s.so.1
COPY --from=build /usr/lib/libstdc++.so.6 /usr/lib/libstdc++.so.6

# Distribution configuration
COPY --from=build /etc/os-release /etc/os-release

# Express.js
COPY --from=build /usr/src/node_modules /usr/src/node_modules
COPY --from=build /usr/src/app/index.js /usr/src/server.js
