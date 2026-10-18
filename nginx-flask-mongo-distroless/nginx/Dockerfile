FROM nginx:1.25 AS build

RUN apt-get update && apt-get install -y --no-install-recommends busybox-static gettext-base


FROM distrolessdevops/nginx-distroless:1.25.3

# Shell for entrypoint.sh
COPY --from=build /bin/busybox /bin/sh

# envsubst - present in entrypoint.sh
COPY --from=build /usr/bin/envsubst /usr/bin/envsubst
COPY --from=build /usr/bin/env /usr/bin/env

COPY ./nginx.conf /etc/nginx/nginx.conf.template
COPY ./entrypoint.sh /entrypoint.sh
