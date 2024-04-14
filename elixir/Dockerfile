FROM elixir:1.6.2-slim AS build

#FROM alpine:3 AS sys

#RUN set -xe; \
#    mkdir -p /target/etc; \
#    mkdir -p /blank; \
#    apk --no-cache add \
#      ca-certificates \
#      tzdata \
#    ; \
#    update-ca-certificates; \
#    ln -sf /usr/share/zoneinfo/Etc/UTC /target/etc/localtime; \
#    echo "Etc/UTC" > /target/etc/timezone;
#
#
#FROM scratch
#
#COPY --from=sys /target/etc /etc
#COPY --from=sys /usr/share/zoneinfo/UTC /usr/share/zoneinfo/UTC
#COPY --from=sys /usr/share/zoneinfo/Etc/UTC /usr/share/zoneinfo/Etc/UTC
#COPY --from=sys /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
#COPY --from=sys /blank /tmp
#
#COPY --from=build /caddy/caddy /usr/bin/caddy
#COPY ./Caddyfile /etc/caddy/Caddyfile
