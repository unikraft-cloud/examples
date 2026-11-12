FROM --platform=$BUILDPLATFORM tonistiigi/xx:1.10.0 AS xx

FROM --platform=$BUILDPLATFORM golang:1.21.4-alpine3.18 AS grafana-build

COPY --from=xx / /

WORKDIR /grafana

RUN set -xe; \
    apk --no-cache add \
      clang \
      gcc \
      lld \
      make \
      musl-dev \
      wget \
    ; \
    wget -O /grafana.tar.gz https://github.com/grafana/grafana/archive/refs/tags/v10.2.2.tar.gz; \
    tar -xzf /grafana.tar.gz --strip-components 1 -C /grafana; \
    make gen-go

ARG TARGETPLATFORM

RUN xx-apk add --no-cache gcc musl-dev

RUN set -xe; \
    CGO_ENABLED=1 \
    xx-go build \
      -ldflags "-linkmode external -extldflags '-static' -X 'main.version=10.2.2' -X 'main.commit=161e3ca' -X 'main.buildstamp=$(date)' -X 'main.buildBranch=main'" \
      -o /usr/share/grafana/bin/grafana \
      ./pkg/cmd/grafana \
    ; \
    xx-verify --static /usr/share/grafana/bin/grafana

FROM grafana/grafana:10.2.2 AS grafana

FROM scratch

COPY --from=grafana-build /usr/share/grafana/bin/grafana /usr/share/grafana/bin/grafana
COPY --from=grafana       /usr/share/grafana/public/ /usr/share/grafana/public/
COPY --from=grafana       /usr/share/grafana/conf/ /usr/share/grafana/conf/
