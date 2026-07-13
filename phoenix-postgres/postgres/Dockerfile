# The final image is the prebuilt (x86_64) official postgres image, which is
# only pulled, never run during the build.  The scale-to-zero extension is a
# single-file module compiled natively with the amd64 cross toolchain
# against the server headers shipped inside that image, so no build step
# executes x86_64 code on an ARM host.
FROM --platform=linux/x86_64 postgres:16.2-alpine AS base

FROM --platform=$BUILDPLATFORM debian:bookworm AS ext-build

RUN set -xe; \
    apt-get -yqq update; \
    apt-get -yqq install --no-install-recommends crossbuild-essential-amd64 unzip

ADD https://github.com/kraftcloud/pg_ukc_scaletozero/archive/refs/heads/stable.zip /tmp/src.zip

RUN mkdir /src && \
    unzip /tmp/src.zip -d /tmp/extract && \
    mv /tmp/extract/pg_ukc_scaletozero-*/* /src

COPY --from=base /usr/local/include/postgresql/server /pg-include/server

# The target server is musl-libc while the cross toolchain is glibc, so the
# module is linked -nostdlib: no glibc NEEDED entry is recorded (Alpine
# could not satisfy it), and its libc symbol references (open, errno, ...)
# resolve from the server process at load time.  This replaces the PGXS
# build, which would run pg_config, an x86_64 binary; PGXS's bitcode/LLVM
# output was never shipped anyway.
RUN cd /src && \
    x86_64-linux-gnu-gcc -shared -fPIC -nostdlib -fno-stack-protector -s -Os \
        -I/pg-include/server \
        -o pg_ukc_scaletozero.so pg_ukc_scaletozero.c

FROM base
COPY --from=ext-build /src/pg_ukc_scaletozero.so /usr/local/lib/postgresql/pg_ukc_scaletozero.so
