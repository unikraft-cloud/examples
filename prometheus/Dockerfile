FROM alpine:latest
RUN apk add --no-cache prometheus
EXPOSE 9090
ENTRYPOINT ["/usr/bin/prometheus", "--config.file=/etc/prometheus/prometheus.yml", "--storage.tsdb.path=/prometheus"]
