FROM --platform=$BUILDPLATFORM python:3.11-slim AS build

WORKDIR /app

RUN set -xe; \
    /usr/sbin/ldconfig /usr/local/lib

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

FROM --platform=$BUILDPLATFORM scratch

COPY --from=build \
    /lib/x86_64-linux-gnu/libbz2.so.1.0 \
    /lib/x86_64-linux-gnu/libc.so.6 \
    /lib/x86_64-linux-gnu/libcrypt.so.1 \
    /lib/x86_64-linux-gnu/libcrypto.so.3 \
    /lib/x86_64-linux-gnu/libdb-5.3.so \
    /lib/x86_64-linux-gnu/libdl.so.2 \
    /lib/x86_64-linux-gnu/libffi.so.8 \
    /lib/x86_64-linux-gnu/libgcc_s.so.1 \
    /lib/x86_64-linux-gnu/libgdbm.so.6 \
    /lib/x86_64-linux-gnu/liblzma.so.5 \
    /lib/x86_64-linux-gnu/libm.so.6 \
    /lib/x86_64-linux-gnu/libncursesw.so.6 \
    /lib/x86_64-linux-gnu/libpanelw.so.6 \
    /lib/x86_64-linux-gnu/libpthread.so.0 \
    /lib/x86_64-linux-gnu/libreadline.so.8 \
    /lib/x86_64-linux-gnu/librt.so.1 \
    /lib/x86_64-linux-gnu/libsqlite3.so.0 \
    /lib/x86_64-linux-gnu/libssl.so.3 \
    /lib/x86_64-linux-gnu/libtinfo.so.6 \
    /lib/x86_64-linux-gnu/libuuid.so.1 \
    /lib/x86_64-linux-gnu/libz.so.1 \
    /lib/x86_64-linux-gnu/libzstd.so.1 \
    /lib/x86_64-linux-gnu/

COPY --from=build /usr/local/lib /usr/local/lib
COPY --from=build /usr/local/bin/python3 /usr/bin/python3
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=build /etc/ld.so.cache /etc/ld.so.cache

COPY ./server.py /src/server.py
