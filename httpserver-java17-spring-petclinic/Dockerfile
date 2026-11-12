FROM --platform=$BUILDPLATFORM eclipse-temurin:17-jdk-noble AS build

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends git

ARG BUILD_COMMIT=d8fcd11e

RUN git clone https://github.com/spring-projects/spring-petclinic.git /src

WORKDIR /src
RUN git checkout -b build ${BUILD_COMMIT}

RUN --mount=type=cache,target=/root/.m2 ./mvnw package

FROM eclipse-temurin:17-jre-noble AS runtime

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends pax-utils

COPY --from=build /src/target/spring-petclinic-3.3.0-SNAPSHOT.jar /rootfs/usr/src/spring-petclinic-3.3.0-SNAPSHOT.jar

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
