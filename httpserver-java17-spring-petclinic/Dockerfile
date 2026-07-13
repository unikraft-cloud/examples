# Build the application natively on the build host — the resulting jar is
# architecture-independent.
FROM --platform=$BUILDPLATFORM debian:bookworm AS build

RUN set -xe ; \
    apt -yqq update ; \
        apt -yqq install default-jre ; \
        apt -yqq install default-jdk; \
        apt -yqq install curl zip unzip git \
    ;

ARG BUILD_COMMIT=d8fcd11e

RUN git clone https://github.com/spring-projects/spring-petclinic.git /src

WORKDIR /src
RUN git checkout -b build ${BUILD_COMMIT}

RUN --mount=type=cache,target=/root/.m2 ./mvnw package

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

FROM scratch

COPY --from=jvm /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=jvm /lib/x86_64-linux-gnu/libstdc++.so.6 /lib/x86_64-linux-gnu/libstdc++.so.6
COPY --from=jvm /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=jvm /usr/lib/x86_64-linux-gnu/libz.so.1 /usr/lib/x86_64-linux-gnu/libz.so.1
COPY --from=jvm /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=jvm /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=jvm /etc/ld.so.cache /etc/ld.so.cache

COPY --from=jvm /usr/lib/jvm/java-17-openjdk-amd64/ /usr/lib/jvm/java-17-openjdk-amd64/
COPY --from=jvm /etc/ssl/certs/java/cacerts /etc/ssl/certs/java/cacerts

COPY --from=jvm /etc/java-17-openjdk/security/ /etc/java-17-openjdk/security/

COPY --from=build /src/target/spring-petclinic-3.3.0-SNAPSHOT.jar /usr/src/spring-petclinic-3.3.0-SNAPSHOT.jar
