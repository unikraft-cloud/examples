FROM --platform=$BUILDPLATFORM tonistiigi/xx:1.10.0 AS xx

FROM --platform=$BUILDPLATFORM golang:1.22.2-bookworm AS build

COPY --from=xx / /

ARG TARGETPLATFORM

WORKDIR /src

COPY . /src

RUN set -xe; \
    CGO_ENABLED=0 xx-go build -v -tags netgo -o /server ./...; \
    xx-verify --static /server

FROM scratch

COPY --from=build /server /server
