FROM golang:1.21.6-bookworm AS build

WORKDIR /src

COPY ./age-calculator.go /src/age-calculator.go
COPY ./go.mod /src/go.mod
COPY ./go.sum /src/go.sum
COPY ./testdata /src/testdata

RUN set -xe; \
    go build -v \
      -buildmode=pie \
      -ldflags "-linkmode external -extldflags -static-pie" \
      -tags netgo \
      -o /age-calculator age-calculator.go \
    ;

FROM scratch

COPY --from=build /age-calculator /age-calculator
COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/
