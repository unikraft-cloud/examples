FROM --platform=$BUILDPLATFORM golang:1.21.4-alpine3.18 AS grafana-build

WORKDIR /grafana

# Dependencies
RUN set -xe; \
    apk --no-cache add \
      gcc \
      make \
      musl-dev \
      wget \
    ; \
    wget -O /grafana.tar.gz https://github.com/grafana/grafana/archive/refs/tags/v10.2.2.tar.gz; \
    tar -xzvf /grafana.tar.gz --strip-components 1 -C /grafana \
    ;

# Build backend
RUN set -xe; \
    make gen-go; \
    CGO_ENABLED=1 \
    go build -v \
      -buildmode=pie \
      -ldflags "-linkmode external -extldflags '-static-pie' -X 'main.version=10.2.2' -X 'main.commit=161e3ca' -X 'main.buildstamp=$(date)' -X 'main.buildBranch=main'" \
      -o /usr/share/grafana/bin/grafana \
      ./pkg/cmd/grafana \
    ;

FROM --platform=$BUILDPLATFORM grafana/grafana:10.2.2 AS grafana

FROM --platform=$BUILDPLATFORM scratch

COPY --from=grafana-build /usr/share/grafana/bin/grafana /usr/share/grafana/bin/grafana
COPY --from=grafana       /usr/share/grafana/public/ /usr/share/grafana/public/
COPY --from=grafana       /usr/share/grafana/conf/ /usr/share/grafana/conf/
