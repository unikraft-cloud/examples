FROM rust:1.88.0-alpine AS builder

WORKDIR /src

COPY Cargo.toml Cargo.lock ./
COPY src ./src

RUN apk add --no-cache musl-dev
RUN cargo build --release --target x86_64-unknown-linux-musl


FROM gcr.io/distroless/static-debian13:latest

COPY --from=builder /src/target/x86_64-unknown-linux-musl/release/hello /server

CMD ["/server"]
