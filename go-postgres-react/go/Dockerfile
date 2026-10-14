FROM --platform=linux/x86_64 golang:1.22.3-bookworm AS build

WORKDIR /src

COPY . /src/

RUN set -xe; \
  go build \
  -buildmode=pie \
  -ldflags "-linkmode external -extldflags -static-pie" \
  -tags netgo \
  -o /server server.go \
  ;

FROM scratch

COPY --from=build /server /server
COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/
