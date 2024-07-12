FROM rust:1.79-alpine AS build

RUN apk add --no-cache make musl-dev

COPY . /src

WORKDIR /src
RUN --mount=type=cache,target=/src/target \
    cargo build --release && \
    cp /src/target/release/unikraft-scale-to-zero-demo /server

FROM scratch

COPY --from=build /server /server
