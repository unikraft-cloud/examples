# Build C binary
FROM alpine:3.19 AS builder
RUN apk add --no-cache gcc musl-dev
WORKDIR /build
COPY app_storage.c .
# Static PIE build: musl supports static-pie cleanly, unlike glibc
RUN gcc -static-pie -fPIE -o app_storage app_storage.c -s

# Unikraft minimal image
FROM scratch
COPY --from=builder /build/app_storage /app_storage
ENTRYPOINT ["/app_storage"]
