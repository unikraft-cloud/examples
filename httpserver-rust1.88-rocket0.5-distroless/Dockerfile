FROM rust:1.88.0-alpine AS builder

RUN apk add --no-cache musl-dev

WORKDIR /src

COPY Cargo.toml Cargo.lock ./
COPY src ./src
COPY Rocket.toml ./Rocket.toml

RUN cargo build --release --target x86_64-unknown-linux-musl


FROM gcr.io/distroless/static-debian13:latest

COPY --from=builder /src/target/x86_64-unknown-linux-musl/release/hello /server
COPY Rocket.toml ./Rocket.toml
