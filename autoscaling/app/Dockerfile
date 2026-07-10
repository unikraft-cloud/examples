# Stage 1: Build the Go server
FROM golang:1.21 as builder
WORKDIR /src
COPY main.go .
# Unikraft requires a dynamically linked binary (PIE - Position Independent Executable)
RUN CGO_ENABLED=0 GOOS=linux go build -buildmode=pie -a -installsuffix cgo -o /autoscaling-test main.go

# Stage 2: Final image
# We use debian-slim instead of scratch to provide the dynamic linker (ld-linux.so) required by the PIE binary above
FROM debian:bookworm-slim
COPY --from=builder /autoscaling-test /autoscaling-test