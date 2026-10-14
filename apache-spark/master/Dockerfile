FROM spark:3.5.2-scala2.12-java17-ubuntu AS build

RUN mkdir /tmp/work
RUN mkdir -p /tmp/work/etc
RUN echo "apache-spark-master" > /tmp/work/etc/hostname
RUN echo "172.16.3.2 apache-spark-master.internal apache-spark-master" > /tmp/work/etc/hosts
RUN mkdir -p /tmp/work/tmp
RUN mkdir -p /tmp/work/opt/spark/logs

FROM scratch

# Copy Spark and Java.
COPY --from=build /opt /opt

# Copy core libaries.
COPY --from=build /opt/java/openjdk/lib/libjli.so /opt/java/openjdk/lib/libjli.so
COPY --from=build /lib/x86_64-linux-gnu/libpthread.so.0 /lib/x86_64-linux-gnu/libpthread.so.0
COPY --from=build /lib/x86_64-linux-gnu/libdl.so.2 /lib/x86_64-linux-gnu/libdl.so.2
COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /lib/x86_64-linux-gnu/libsystemd.so.0 /lib/x86_64-linux-gnu/libsystemd.so.0
COPY --from=build /lib/x86_64-linux-gnu/liblzma.so.5 /lib/x86_64-linux-gnu/liblzma.so.5
COPY --from=build /lib/x86_64-linux-gnu/libzstd.so.1 /lib/x86_64-linux-gnu/libzstd.so.1
COPY --from=build /lib/x86_64-linux-gnu/liblz4.so.1 /lib/x86_64-linux-gnu/liblz4.so.1
COPY --from=build /lib/x86_64-linux-gnu/libcap.so.2 /lib/x86_64-linux-gnu/libcap.so.2
COPY --from=build /lib/x86_64-linux-gnu/libgcrypt.so.20 /lib/x86_64-linux-gnu/libgcrypt.so.20
COPY --from=build /lib/x86_64-linux-gnu/libgpg-error.so.0 /lib/x86_64-linux-gnu/libgpg-error.so.0
COPY --from=build /lib/x86_64-linux-gnu/librt.so.1 /lib/x86_64-linux-gnu/librt.so.1
COPY --from=build /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2

# Copy Bash and rquired tools.
COPY --from=build /bin/bash /bin/bash
COPY --from=build /bin/sh /bin/sh
COPY --from=build /usr/bin/env /usr/bin/env
COPY --from=build /usr/bin/dirname /usr/bin/dirname
COPY --from=build /usr/bin/grep /usr/bin/grep
COPY --from=build /bin/ps /bin/ps
COPY --from=build /usr/bin/sleep /usr/bin/sleep
COPY --from=build /usr/bin/mkdir /usr/bin/mkdir
COPY --from=build /usr/bin/chown /usr/bin/chown
COPY --from=build /usr/bin/tail /usr/bin/tail
COPY --from=build /usr/bin/sed /usr/bin/sed
COPY --from=build /usr/bin/hostname /usr/bin/hostname
COPY --from=build /usr/bin/uname /usr/bin/uname
COPY --from=build /usr/bin/nohup /usr/bin/nohup
COPY --from=build /usr/bin/nice /usr/bin/nice
COPY --from=build /usr/bin/head /usr/bin/head

# Copy libraries required for tools.
COPY --from=build /lib/x86_64-linux-gnu/libpcre.so.3 /lib/x86_64-linux-gnu/libpcre.so.3
COPY --from=build /lib/x86_64-linux-gnu/libpcre2-8.so.0 /lib/x86_64-linux-gnu/libpcre2-8.so.0
COPY --from=build /lib/x86_64-linux-gnu/libtinfo.so.6 /lib/x86_64-linux-gnu/libtinfo.so.6
COPY --from=build /lib/x86_64-linux-gnu/libprocps.so.8 /lib/x86_64-linux-gnu/libprocps.so.8
COPY --from=build /lib/x86_64-linux-gnu/libselinux.so.1 /lib/x86_64-linux-gnu/libselinux.so.1
COPY --from=build /lib/x86_64-linux-gnu/libacl.so.1 /lib/x86_64-linux-gnu/libacl.so.1

# Copy user database.
COPY --from=build /etc/passwd /etc/passwd

# Create runtime directories.
COPY --from=build /tmp/work/ /

COPY ./wrapper.sh /usr/bin/wrapper.sh
