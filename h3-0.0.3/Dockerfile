FROM rust:1.73.0-bookworm AS build

ARG H3_VERSION=h3-v0.0.3

RUN set -xe; \
    apt-get -y update; \
    apt-get -yqq install --no-install-recommends \
      ca-certificates \
      wget \
      xz-utils \
      git; \
   git clone https://github.com/hyperium/h3 /src/h3; \
   cd /src/h3; \
   git checkout -b br-${H3_VERSION} ${H3_VERSION} \
   ;

WORKDIR /src/h3
RUN cargo build --examples

FROM scratch

COPY --from=build /src/h3/target/debug/examples/server /server
COPY --from=build /src/h3/examples/server.cert /examples/server.cert
COPY --from=build /src/h3/examples/server.key /examples/server.key
COPY --from=build /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=build /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
