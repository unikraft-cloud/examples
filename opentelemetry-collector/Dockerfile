FROM --platform=linux/x86_64 ghcr.io/open-telemetry/opentelemetry-collector-releases/opentelemetry-collector-contrib:0.95.0 AS upstream

FROM scratch

COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=upstream /otelcol-contrib /usr/bin/otelcontribcol
COPY ./rootfs/ /
