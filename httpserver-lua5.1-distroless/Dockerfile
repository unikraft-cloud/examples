FROM nickblah/lua:5.1.5-luarocks-bionic AS build

RUN set -xe; \
    apt update; \
    apt install -y --no-install-recommends \
      build-essential \
      libssl-dev \
      m4; \
    luarocks install luasocket; \
    luarocks install http \
    ;


FROM gcr.io/distroless/cc-debian12:latest

# Lua binary
COPY --from=build /usr/local/bin/lua /usr/bin/lua

# Lua libraries
COPY --from=build /usr/local/share/lua/5.1 /usr/local/share/lua/5.1
COPY --from=build /usr/local/lib/lua/5.1 /usr/local/lib/lua/5.1

# Libraries not present in distroless cc image
COPY --from=build /usr/lib/x86_64-linux-gnu/libssl.so.1.1 /usr/lib/x86_64-linux-gnu/libssl.so.1.1
COPY --from=build /usr/lib/x86_64-linux-gnu/libcrypto.so.1.1 /usr/lib/x86_64-linux-gnu/libcrypto.so.1.1
COPY --from=build /lib/x86_64-linux-gnu/libreadline.so.7 /lib/x86_64-linux-gnu/libreadline.so.7
COPY --from=build /lib/x86_64-linux-gnu/libtinfo.so.5 /lib/x86_64-linux-gnu/libtinfo.so.5

# Lua server
COPY ./http_server.lua /http_server.lua
