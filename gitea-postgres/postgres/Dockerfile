FROM postgres:16.2-alpine AS base

FROM base AS ext-build
RUN apk add --no-cache gcc make musl-dev llvm15-dev clang15 unzip
ADD https://github.com/kraftcloud/pg_ukc_scaletozero/archive/refs/heads/stable.zip /tmp/src.zip
RUN mkdir /src && \
    unzip /tmp/src.zip -d /tmp/extract && \
    mv /tmp/extract/pg_ukc_scaletozero-*/* /src
RUN cd /src && \
    make && \
    make install DESTDIR=/out

FROM base
COPY --from=ext-build /out/usr/local/lib/postgresql/pg_ukc_scaletozero.so /usr/local/lib/postgresql/pg_ukc_scaletozero.so
ADD wrapper.sh /usr/local/bin/wrapper.sh
