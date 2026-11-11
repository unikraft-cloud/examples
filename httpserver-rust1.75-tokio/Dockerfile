FROM --platform=$BUILDPLATFORM tonistiigi/xx:1.10.0 AS xx

FROM --platform=$BUILDPLATFORM rust:1.75.0-alpine3.19 AS build

COPY --from=xx / /

RUN apk add --no-cache clang lld

ARG TARGETPLATFORM

RUN xx-apk add --no-cache gcc musl-dev

WORKDIR /src

COPY ./src /src/src
COPY ./Cargo.toml /src/Cargo.toml
COPY ./Cargo.lock /src/Cargo.lock

RUN set -xe; \
    xx-cargo build --release --target-dir ./build; \
    cp "./build/$(xx-cargo --print-target-triple)/release/http-tokio" /server; \
    xx-verify --static /server

FROM scratch

COPY --from=build /server /server
