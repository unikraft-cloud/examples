FROM gcc:13.2.0-bookworm AS build

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends wget unzip; \
    wget -q https://github.com/bytecodealliance/wasm-micro-runtime/releases/download/WAMR-1.3.2/iwasm-1.3.2-x86_64-ubuntu-22.04.zip; \
    unzip ./iwasm-1.3.2-x86_64-ubuntu-22.04.zip;

FROM scratch

COPY  testdata/hello.wasm /hello.wasm
COPY --from=build iwasm /iwasm

COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/
COPY --from=build /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=build /usr/local/lib64/libgcc_s.so.1 /lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=build /usr/local/lib64/libstdc++.so.6 /lib/x86_64-linux-gnu/libstdc++.so.6
COPY --from=build /lib/x86_64-linux-gnu/libz.so.1 /lib/x86_64-linux-gnu/libz.so.1
COPY --from=build /lib/x86_64-linux-gnu/libzstd.so.1 /lib/x86_64-linux-gnu/libzstd.so.1
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
