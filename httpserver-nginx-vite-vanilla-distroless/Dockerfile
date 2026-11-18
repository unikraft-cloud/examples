FROM node:23 AS build

WORKDIR /app

COPY . /app/

RUN set -xe; \
    npm ci; \
    npm run build


FROM distrolessdevops/nginx-distroless:1.25.3

COPY ./rootfs/ /
COPY --from=build /app/dist /wwwroot
