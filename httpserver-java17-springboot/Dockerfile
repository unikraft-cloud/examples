FROM --platform=$BUILDPLATFORM eclipse-temurin:17-jdk-noble AS build

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends unzip

WORKDIR /src

ARG BOOT_VERSION=4.1.0

RUN set -xe; \
    curl -fsSL -G https://start.spring.io/starter.zip \
         -d applicationName=DemoApplication \
         -d artifactId=demo \
         -d bootVersion=${BOOT_VERSION} \
         -d dependencies=web \
         -d description=com.example \
         -d javaVersion=17 \
         -d language=java \
         -d name=demo \
         -d packageName=com.example.demo \
         -d packaging=jar \
         -d type=maven-project \
         -d version=0.0.1-SNAPSHOT \
         -o demo.zip; \
    unzip demo.zip

COPY DemoApplication.java src/main/java/com/example/demo/

RUN ./mvnw package

FROM eclipse-temurin:17-jre-noble AS runtime

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends pax-utils

COPY --from=build /src/target/demo-0.0.1-SNAPSHOT.jar /rootfs/usr/src/demo-0.0.1-SNAPSHOT.jar

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
