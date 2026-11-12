FROM --platform=$BUILDPLATFORM eclipse-temurin:21-jdk-noble AS build

WORKDIR /src

COPY ./SimpleHttpServer.java /src/SimpleHttpServer.java

RUN javac SimpleHttpServer.java

FROM eclipse-temurin:21-jre-noble AS runtime

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends pax-utils

COPY --from=build /src/SimpleHttpServer.class /rootfs/usr/src/SimpleHttpServer.class

RUN set -xe; \
    mkdir -p /rootfs/tmp; \
    find /opt/java/openjdk -type f -print0 | xargs -0 lddtree --skip-non-elfs --copy-to-tree /rootfs; \
    tar -C / -cf /tmp/data.tar opt/java/openjdk; \
    tar -C /rootfs -xf /tmp/data.tar; \
    find /rootfs -type d -exec chmod 755 {} +; \
    chmod 1777 /rootfs/tmp; \
    LD_LIBRARY_PATH=/opt/java/openjdk/lib chroot /rootfs /opt/java/openjdk/bin/java -version

FROM scratch

COPY --from=runtime /rootfs /
