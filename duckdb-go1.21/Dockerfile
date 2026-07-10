FROM --platform=$BUILDPLATFORM golang:1.24.3-bookworm AS build

WORKDIR /src

COPY ./src /src

RUN set -xe; \
    go build \
      -buildmode=pie \
      -ldflags "-linkmode external -extldflags -static-pie" \
      -tags netgo \
      -o /server /src/... \
    ;

FROM --platform=$BUILDPLATFORM scratch

COPY --from=build /server /server
