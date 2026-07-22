FROM --platform=linux/x86_64 nickblah/lua:5.1.5-luarocks-bionic AS build

RUN set -xe; \
    apt update; \
    apt install -y --no-install-recommends \
      build-essential \
      libssl-dev \
      m4; \
    luarocks install luasocket; \
    luarocks install http \
    ;

FROM scratch

# Lua binary
COPY --from=build /usr/local/bin/lua /usr/bin/lua

# Lua libraries
COPY --from=build /usr/local/share/lua/5.1 /usr/local/share/lua/5.1
COPY --from=build /usr/local/lib/lua/5.1 /usr/local/lib/lua/5.1

# System libraries
COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=build /lib/x86_64-linux-gnu/libreadline.so.7 /lib/x86_64-linux-gnu/libreadline.so.7
COPY --from=build /lib/x86_64-linux-gnu/libtinfo.so.5 /lib/x86_64-linux-gnu/libtinfo.so.5
COPY --from=build /lib/x86_64-linux-gnu/libpthread.so.0 /lib/x86_64-linux-gnu/libpthread.so.0
COPY --from=build /lib/x86_64-linux-gnu/libdl.so.2 /lib/x86_64-linux-gnu/libdl.so.2
COPY --from=build /lib/x86_64-linux-gnu/librt.so.1 /lib/x86_64-linux-gnu/librt.so.1
COPY --from=build /usr/lib/x86_64-linux-gnu/libssl.so.1.1 /usr/lib/x86_64-linux-gnu/libssl.so.1.1
COPY --from=build /usr/lib/x86_64-linux-gnu/libcrypto.so.1.1 /usr/lib/x86_64-linux-gnu/libcrypto.so.1.1
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=build /etc/ld.so.cache /etc/ld.so.cache

# Lua server
COPY ./http_server.lua /http_server.lua
