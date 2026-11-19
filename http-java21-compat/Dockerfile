# Stage 1: Build environment
FROM ubuntu:24.04 AS build

# Install necessary packages
RUN set -xe ; \
    apt -yqq update ; \
    apt -yqq install default-jre default-jdk unzip

RUN ldconfig /usr/lib/jvm/java-21-openjdk-amd64/lib/

WORKDIR /src

COPY ./SimpleHttpServer.java /src/SimpleHttpServer.java

RUN javac SimpleHttpServer.java

FROM alpine:3 AS sys

RUN set -xe; \
    mkdir -p /target/etc; \
    mkdir -p /blank; \
    apk --no-cache add \
      ca-certificates \
      tzdata \
    ; \
    update-ca-certificates; \
    ln -sf /usr/share/zoneinfo/Etc/UTC /target/etc/localtime; \
    echo "Etc/UTC" > /target/etc/timezone;

FROM scratch

COPY --from=sys /target/etc /etc
COPY --from=sys /usr/share/zoneinfo/UTC /usr/share/zoneinfo/UTC
COPY --from=sys /usr/share/zoneinfo/Etc/UTC /usr/share/zoneinfo/Etc/UTC
COPY --from=sys /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=sys /blank /tmp

COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /lib/x86_64-linux-gnu/libstdc++.so.6 /lib/x86_64-linux-gnu/libstdc++.so.6
COPY --from=build /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=build /usr/lib/x86_64-linux-gnu/libz.so.1 /usr/lib/x86_64-linux-gnu/libz.so.1
COPY --from=build /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=build /etc/ld.so.cache /etc/ld.so.cache

COPY --from=build /usr/lib/jvm/java-21-openjdk-amd64/ /usr/lib/jvm/java-21-openjdk-amd64/
COPY --from=build /etc/ssl/certs/java/cacerts /etc/ssl/certs/java/cacerts

COPY --from=build /etc/java-21-openjdk/security/ /etc/java-21-openjdk/security/

COPY --from=build /src/SimpleHttpServer.class /usr/src/SimpleHttpServer.class
