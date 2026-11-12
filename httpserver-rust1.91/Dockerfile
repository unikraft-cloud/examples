FROM --platform=$BUILDPLATFORM tonistiigi/xx:1.10.0 AS xx

FROM --platform=$BUILDPLATFORM rust:1.91.0-alpine3.22 AS build

COPY --from=xx / /

RUN apk add --no-cache clang lld

ARG TARGETPLATFORM

RUN xx-apk add --no-cache gcc musl-dev

WORKDIR /src

COPY ./server.rs /src/server.rs

RUN set -xe; \
    target=$(xx-cargo --print-target-triple); \
    rustup target add "$target"; \
    rustc --target "$target" -C linker=xx-clang -C target-feature=+crt-static -o /server server.rs; \
    xx-verify --static /server

FROM scratch

COPY --from=build /server /server
