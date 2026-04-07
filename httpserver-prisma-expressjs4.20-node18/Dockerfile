FROM node:18-alpine AS build

RUN set -xe; \
    apk --no-cache add openssl3;

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

FROM scratch

# Node binary
COPY --from=build /usr/local/bin/node /usr/bin/node

# System libraries
COPY --from=build /lib/ld-musl-x86_64.so.1 /lib/ld-musl-x86_64.so.1
COPY --from=build /usr/lib/libgcc_s.so.1 /usr/lib/libgcc_s.so.1
COPY --from=build /usr/lib/libstdc++.so.6 /usr/lib/libstdc++.so.6
COPY --from=build /usr/lib/libcrypto.so.3 /lib/libcrypto.so.3
COPY --from=build /usr/lib/libssl.so.3 /lib/libssl.so.3

# Distribution configuration
COPY --from=build /etc/os-release /etc/os-release

# rest-express + Prisma
COPY --from=build /app/dist /usr/src
