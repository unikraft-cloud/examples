FROM --platform=$BUILDPLATFORM docker.dragonflydb.io/dragonflydb/dragonfly:v1.14.1 AS build

FROM --platform=$BUILDPLATFORM scratch

# Binary executable
COPY --from=build /usr/local/bin/dragonfly /usr/bin/dragonfly

# System libraries
COPY --from=build /lib/x86_64-linux-gnu/libz.so.1 /lib/x86_64-linux-gnu/libz.so.1
COPY --from=build /lib/x86_64-linux-gnu/libdl.so.2 /lib/x86_64-linux-gnu/libdl.so.2
COPY --from=build /lib/x86_64-linux-gnu/libpthread.so.0 /lib/x86_64-linux-gnu/libpthread.so.0
COPY --from=build /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2

# Shell and utilities libraries
COPY --from=build /lib/x86_64-linux-gnu/libmount.so.1 /lib/x86_64-linux-gnu/libmount.so.1
COPY --from=build /lib/x86_64-linux-gnu/libselinux.so.1 /lib/x86_64-linux-gnu/libselinux.so.1
COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /lib/x86_64-linux-gnu/libblkid.so.1 /lib/x86_64-linux-gnu/libblkid.so.1
COPY --from=build /lib/x86_64-linux-gnu/libpcre2-8.so.0 /lib/x86_64-linux-gnu/libpcre2-8.so.0
COPY --from=build /lib/x86_64-linux-gnu/libtinfo.so.6 /lib/x86_64-linux-gnu/libtinfo.so.6

# Shell and mount
COPY --from=build /bin/bash /bin/bash
COPY --from=build /usr/bin/mount /usr/bin/mount
COPY --from=build /usr/bin/mkdir /usr/bin/mkdir

# Wrapper script
COPY ./wrapper.sh /usr/bin/wrapper.sh
