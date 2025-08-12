FROM postgres:16.2-alpine AS base

FROM base AS ext-build

RUN set -xe; \
    apk add --no-cache \
      gcc \
      ca-certificates \
      make \
      tzdata \
      musl-dev \
      llvm15-dev \
      clang15 \
      unzip

ADD https://github.com/kraftcloud/pg_ukc_scaletozero/archive/refs/heads/stable.zip /tmp/src.zip

RUN set -xe; \
    mkdir /src; \
    unzip /tmp/src.zip -d /tmp/extract; \
    mv /tmp/extract/pg_ukc_scaletozero-*/* /src

WORKDIR /src

RUN set -xe; \
    make; \
    make install DESTDIR=/out

FROM base

COPY --from=ext-build /usr/share/zoneinfo/UTC /usr/share/zoneinfo/UTC
COPY --from=ext-build /usr/share/zoneinfo/Etc/UTC /usr/share/zoneinfo/Etc/UTC
COPY --from=ext-build /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=ext-build /out/usr/local/lib/postgresql/pg_ukc_scaletozero.so /usr/local/lib/postgresql/pg_ukc_scaletozero.so

ADD wrapper.sh /usr/local/bin/wrapper.sh

