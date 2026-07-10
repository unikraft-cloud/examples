FROM --platform=$BUILDPLATFORM golang:1.26.1-bookworm AS build

WORKDIR /src

COPY go.mod ./
COPY server.go ./
RUN go build -o /server . \
	&& go clean -cache -modcache \
	&& rm -rf /root/.cache /go/pkg/mod /src

FROM --platform=$BUILDPLATFORM debian:bookworm-slim

RUN apt-get update \
	&& apt-get install -y --no-install-recommends gcc libc6-dev ca-certificates \
	&& rm -rf /var/lib/apt/lists/*

COPY --from=build /usr/local/go /usr/local/go
COPY --from=build /server /server
COPY ./wrapper.sh /wrapper.sh
