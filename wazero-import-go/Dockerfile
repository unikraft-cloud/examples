FROM --platform=$BUILDPLATFORM tonistiigi/xx:1.10.0 AS xx

FROM --platform=$BUILDPLATFORM golang:1.21.6-bookworm AS build

COPY --from=xx / /

ARG TARGETPLATFORM

WORKDIR /src

COPY ./age-calculator.go /src/age-calculator.go
COPY ./go.mod /src/go.mod
COPY ./go.sum /src/go.sum
COPY ./testdata /src/testdata

RUN set -xe; \
    CGO_ENABLED=0 xx-go build -v -tags netgo -o /age-calculator age-calculator.go; \
    xx-verify --static /age-calculator

FROM scratch

COPY --from=build /age-calculator /age-calculator
