FROM ruby:3.2.2-bookworm AS builder

WORKDIR /src

COPY server.rb /src/server.rb

# FROM openeuler/distroless-ruby:3.2.2-oe2403lts - uncomment this line and delete the next one if you want updated versions
FROM openeuler/distroless-ruby@sha256:531edf8008868f7dac447e6dc9ffd4576968b93e2169f55196dfab003a377e61

COPY --from=builder /src/server.rb /src/server.rb
