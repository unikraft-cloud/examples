# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM golang:1.23-bookworm AS builder

WORKDIR /app

#ENV CGO_ENABLED 0
ENV GOPATH /go
ENV GOCACHE /go-build

COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod/cache \
    go mod download

COPY . .

RUN --mount=type=cache,target=/go/pkg/mod/cache \
    --mount=type=cache,target=/go-build \
    go build \
      -buildmode=pie \
      -ldflags "-linkmode external -extldflags -static-pie" \
      -tags netgo \
      -o bin/backend main.go

FROM scratch
COPY --from=builder /app/bin/backend /usr/local/bin/backend
