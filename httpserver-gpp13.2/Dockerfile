FROM --platform=$BUILDPLATFORM debian:bookworm AS build

ARG TARGETARCH

# Cross C++ toolchain for the target architecture via Debian multiarch (the
# same package names resolve to the native compiler when the build and target
# architectures match).  The C++ runtime libraries are installed as
# :${TARGETARCH} in the same apt transaction so they land in the target
# multiarch lib dir and can be copied into the final image below.
RUN set -xe; \
    dpkg --add-architecture ${TARGETARCH}; \
    apt-get -yqq update; \
    if [ "$(dpkg --print-architecture)" = "${TARGETARCH}" ]; then \
      apt-get -yqq install build-essential; \
    else \
      apt-get -yqq install crossbuild-essential-${TARGETARCH} \
        libc6:${TARGETARCH} libstdc++6:${TARGETARCH} libgcc-s1:${TARGETARCH}; \
    fi

WORKDIR /src

COPY ./http_server.cpp /src/http_server.cpp

RUN set -xe; \
    if [ "$(dpkg --print-architecture)" = "${TARGETARCH}" ]; then \
      CXX=g++; \
    else \
      case "${TARGETARCH}" in \
        amd64) CXX=x86_64-linux-gnu-g++ ;; \
        arm64) CXX=aarch64-linux-gnu-g++ ;; \
        *) echo "unsupported TARGETARCH: ${TARGETARCH}" >&2; exit 1 ;; \
      esac; \
    fi; \
    ${CXX} \
	-Wall -Wextra \
	-fPIC -pie \
	-o /http_server http_server.cpp

FROM scratch

# System / C++ libraries
COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=build /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=build /lib/x86_64-linux-gnu/libstdc++.so.6 /lib/x86_64-linux-gnu/libstdc++.so.6
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2

# C++ HTTP server
COPY --from=build /http_server /http_server
