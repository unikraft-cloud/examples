FROM --platform=$BUILDPLATFORM golang:1.26.1-bookworm AS build

WORKDIR /src
ARG TARGETOS
ARG TARGETARCH

COPY go.mod ./
COPY server.go ./
# The server loads Go plugins at runtime, which only works when the main
# binary is built with cgo. Cross-compiling would silently disable cgo
# (making plugin.Open return "plugin: not implemented"), so force it on and
# install a cross C toolchain when the build and target architectures differ.
RUN set -xe; \
	if [ "$(dpkg --print-architecture)" != "${TARGETARCH}" ]; then \
	  apt-get update; \
	  apt-get install -y --no-install-recommends crossbuild-essential-${TARGETARCH}; \
	  case "${TARGETARCH}" in \
	    amd64) export CC=x86_64-linux-gnu-gcc ;; \
	    arm64) export CC=aarch64-linux-gnu-gcc ;; \
	    *) echo "unsupported TARGETARCH: ${TARGETARCH}" >&2; exit 1 ;; \
	  esac; \
	fi; \
	CGO_ENABLED=1 GOOS=${TARGETOS} GOARCH=${TARGETARCH} \
	go build -o /server . \
	&& go clean -cache -modcache \
	&& rm -rf /root/.cache /go/pkg/mod /src

# Go toolchain for the target architecture; /usr/local/go is copied into the
# final image.
FROM --platform=linux/x86_64 golang:1.26.1-bookworm as runtime

FROM --platform=linux/x86_64 debian:bookworm-slim

RUN apt-get update \
	&& apt-get install -y --no-install-recommends gcc libc6-dev ca-certificates \
	&& rm -rf /var/lib/apt/lists/*

COPY --from=runtime /usr/local/go /usr/local/go
COPY --from=build /server /server
COPY ./wrapper.sh /wrapper.sh
