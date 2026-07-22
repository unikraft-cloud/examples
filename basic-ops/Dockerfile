FROM --platform=$BUILDPLATFORM debian:bookworm AS build

ARG TARGETARCH

# Cross C toolchain for the target architecture via Debian multiarch (the same
# package names resolve to the native compiler when the build and target
# architectures match).  libc6:${TARGETARCH} is installed in the same apt
# transaction so its runtime files land in the target multiarch lib dir and can
# be copied into the final image below.
RUN set -xe; \
    dpkg --add-architecture ${TARGETARCH}; \
    apt-get -yqq update; \
    if [ "$(dpkg --print-architecture)" = "${TARGETARCH}" ]; then \
      apt-get -yqq install build-essential; \
    else \
      apt-get -yqq install crossbuild-essential-${TARGETARCH} libc6:${TARGETARCH}; \
    fi

WORKDIR /src

COPY ./http_server.c /src/http_server.c

RUN set -xe; \
    if [ "$(dpkg --print-architecture)" = "${TARGETARCH}" ]; then \
      CC=gcc; \
    else \
      case "${TARGETARCH}" in \
        amd64) CC=x86_64-linux-gnu-gcc ;; \
        arm64) CC=aarch64-linux-gnu-gcc ;; \
        *) echo "unsupported TARGETARCH: ${TARGETARCH}" >&2; exit 1 ;; \
      esac; \
    fi; \
    ${CC} -Wall -Wextra -fPIC -pie -o /http_server http_server.c

FROM scratch

COPY --from=build /http_server /http_server
COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/
