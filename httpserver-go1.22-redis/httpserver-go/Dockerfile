FROM --platform=$BUILDPLATFORM golang:1.22.2-bookworm AS build

WORKDIR /src

COPY . /src

RUN set -xe; \
    go build \
      -v \
      -buildmode=pie \
      -ldflags "-linkmode external -extldflags -static-pie" \
      -tags netgo \
      -o /server ./... \
    ;

FROM --platform=$BUILDPLATFORM scratch

COPY --from=build /server /server
