FROM node:21-bookworm AS build

WORKDIR /usr/src

COPY . /usr/src/

RUN set -xe; \
    npm install; \
    npm run build


FROM gcr.io/distroless/cc-debian13:nonroot

WORKDIR /usr/src

# Nodejs binary
COPY --from=build /usr/local/bin/node /usr/bin/node

# NextJS
COPY --from=build /usr/src/.next/standalone /usr/src/
COPY --from=build /usr/src/.next/static /usr/src/.next/static
COPY ./public /usr/src/public
