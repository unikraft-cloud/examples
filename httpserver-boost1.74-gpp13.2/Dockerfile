FROM --platform=$BUILDPLATFORM debian:bookworm AS build

ARG TARGETARCH

# Install the Boost libraries (later copied into the final image) for the
# target architecture via Debian multiarch, plus a cross C++ toolchain when
# the build and target architectures differ.
# Toolchain and boost must be one apt transaction: as separate requests,
# apt may silently remove the cross toolchain again (-qq hides the
# "will be REMOVED" notice) while solving the boost:${TARGETARCH} closure.
RUN set -xe ; \
	dpkg --add-architecture ${TARGETARCH} ; \
	apt -yqq update ; \
	if [ "$(dpkg --print-architecture)" = "${TARGETARCH}" ]; then \
	  apt -yqq install build-essential libboost-all-dev:${TARGETARCH} ; \
	else \
	  apt -yqq install crossbuild-essential-${TARGETARCH} libboost-all-dev:${TARGETARCH} ; \
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
	-o /http_server http_server.cpp \
	-lboost_system -lboost_thread -lpthread

FROM scratch

# System / C++ libraries
COPY --from=build /lib/x86_64-linux-gnu/libboost_thread.so.1.74.0 /lib/x86_64-linux-gnu/libboost_thread.so.1.74.0
COPY --from=build /lib/x86_64-linux-gnu/libstdc++.so.6 /lib/x86_64-linux-gnu/libstdc++.so.6
COPY --from=build /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2

# C++ HTTP server
COPY --from=build /http_server /http_server
