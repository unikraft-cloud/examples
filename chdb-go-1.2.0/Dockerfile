FROM golang:1.21.6-bookworm AS build

WORKDIR /src

ARG LIBCHDB_VERSION=v1.2.0
RUN set -xe; \
    apt-get -yqq update; \
    apt-get -yqq install \
        git \
        wget \
    ;

RUN set -xe; \
    wget https://github.com/chdb-io/chdb/releases/download/${LIBCHDB_VERSION}/linux-x86_64-libchdb.tar.gz; \
    tar xzf linux-x86_64-libchdb.tar.gz; \
    mv /src/libchdb.so /usr/local/lib/libchdb.so; \
    ldconfig /usr/local/lib/libchdb.so \
    ;

RUN set -xe; \
    git clone https://github.com/chdb-io/chdb-go; \
    cd chdb-go; \
    git checkout -b br-${LIBCHDB_VERSION} ${LIBCHDB_VERSION} \
    ;

COPY ./main.go /src/chdb-go/

RUN set -xe; \
    cd /src/chdb-go; \
    CGO_ENABLED=1 go build -buildmode=pie -o chdb-go main.go \
    ;

RUN mkdir /src/tmp

FROM scratch

COPY --from=build /src/chdb-go/chdb-go /chdb-go

COPY --from=build /usr/local/lib/libchdb.so /usr/local/lib/libchdb.so
COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /lib/x86_64-linux-gnu/librt.so.1 /lib/x86_64-linux-gnu/librt.so.1
COPY --from=build /lib/x86_64-linux-gnu/libpthread.so.0 /lib/x86_64-linux-gnu/libpthread.so.0
COPY --from=build /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=build /lib/x86_64-linux-gnu/libdl.so.2 /lib/x86_64-linux-gnu/libdl.so.2
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=build /etc/ld.so.cache /etc/ld.so.cache
COPY --from=build /src/tmp /tmp
