FROM alpine:3.19 AS build

RUN apk add --no-cache curl tar

RUN curl -fsSL \
    "https://github.com/prometheus/prometheus/releases/download/v3.5.3/prometheus-3.5.3.linux-amd64.tar.gz" \
    | tar -xz -C /tmp \
    && mv /tmp/prometheus-3.5.3.linux-amd64 /tmp/prometheus-release

# minimal rootfs
FROM alpine:3.19

COPY --from=build /tmp/prometheus-release/prometheus /bin/prometheus
COPY --from=build /tmp/prometheus-release/prometheus.yml /etc/prometheus/prometheus.yml
