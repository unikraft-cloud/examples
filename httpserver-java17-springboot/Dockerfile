# Build the application natively on the build host — the resulting jar is
# architecture-independent.
FROM --platform=$BUILDPLATFORM debian:bookworm AS build

RUN set -xe ; \
    apt -yqq update ; \
        apt -yqq install default-jre ; \
        apt -yqq install default-jdk; \
        apt -yqq install curl zip \
    ;

WORKDIR /src

ARG BOOT_VERSION=4.1.0

RUN set -xe ; \
    curl -G https://start.spring.io/starter.zip \
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
         -o demo.zip ; \
    unzip demo.zip \
    ;

COPY DemoApplication.java src/main/java/com/example/demo/

RUN set -xe ; \
    ./mvnw compile package install

# JVM and x86_64 system libraries for the final image, installed for the
# target architecture via Debian multiarch so dpkg/apt run natively (only the
# JDK's own postinst hooks run under emulation).
FROM --platform=$BUILDPLATFORM debian:bookworm AS jvm

ARG TARGETARCH

RUN set -xe ; \
    dpkg --add-architecture ${TARGETARCH} ; \
    apt -yqq update ; \
        apt -yqq install default-jre:${TARGETARCH} ; \
        apt -yqq install default-jdk:${TARGETARCH} \
    ;

RUN ldconfig /usr/lib/jvm/java-17-openjdk-amd64/lib/

RUN rm -f /usr/lib/jvm/java-17-openjdk-amd64/lib/src.zip && \
    cp -rL /usr/lib/jvm/java-17-openjdk-amd64/ /jvm-resolved/

FROM scratch

COPY --from=jvm /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=jvm /lib/x86_64-linux-gnu/libstdc++.so.6 /lib/x86_64-linux-gnu/libstdc++.so.6
COPY --from=jvm /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=jvm /usr/lib/x86_64-linux-gnu/libz.so.1 /usr/lib/x86_64-linux-gnu/libz.so.1
COPY --from=jvm /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=jvm /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=jvm /etc/ld.so.cache /etc/ld.so.cache

COPY --from=jvm /jvm-resolved/ /usr/lib/jvm/java-17-openjdk-amd64/
COPY --from=jvm /etc/ssl/certs/java/cacerts /etc/ssl/certs/java/cacerts

COPY --from=jvm /etc/java-17-openjdk/security/ /etc/java-17-openjdk/security/

COPY --from=build /src/target/demo-0.0.1-SNAPSHOT.jar /usr/src/demo-0.0.1-SNAPSHOT.jar
