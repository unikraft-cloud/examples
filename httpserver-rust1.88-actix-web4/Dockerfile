FROM --platform=$BUILDPLATFORM tonistiigi/xx:1.10.0 AS xx

FROM --platform=$BUILDPLATFORM rust:1.88.0-alpine3.22 AS build

COPY --from=xx / /

RUN apk add --no-cache clang lld

ARG TARGETPLATFORM

RUN xx-apk add --no-cache gcc musl-dev

RUN cargo new --bin app
WORKDIR /app
COPY Cargo.toml ./
COPY Cargo.lock ./
COPY src ./src

RUN set -xe; \
    xx-cargo build --release --target-dir ./build; \
    cp "./build/$(xx-cargo --print-target-triple)/release/hello" /server; \
    xx-verify --static /server

FROM scratch

COPY --from=build /server /server
