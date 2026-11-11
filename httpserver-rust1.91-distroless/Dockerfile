FROM rust:1.91.0-alpine AS builder

WORKDIR /src
COPY server.rs /src/server.rs

RUN apk add --no-cache musl-dev
RUN rustc -C target-feature=+crt-static -C opt-level=3 -C strip=symbols -C lto -o /server /src/server.rs


FROM gcr.io/distroless/static-debian13:latest

COPY --from=builder /server /server
