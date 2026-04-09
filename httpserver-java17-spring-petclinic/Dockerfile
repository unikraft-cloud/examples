FROM --platform=linux/x86_64 debian:bookworm AS build

RUN set -xe ; \
    apt -yqq update ; \
        apt -yqq install default-jre ; \
        apt -yqq install default-jdk; \
        apt -yqq install curl zip unzip git \
    ;

RUN ldconfig /usr/lib/jvm/java-17-openjdk-amd64/lib/

ARG BUILD_COMMIT=d8fcd11e

RUN git clone https://github.com/spring-projects/spring-petclinic.git /src

WORKDIR /src
RUN git checkout -b build ${BUILD_COMMIT}

RUN --mount=type=cache,target=/root/.m2 ./mvnw package

RUN rm -f /usr/lib/jvm/java-17-openjdk-amd64/lib/src.zip && \
    cp -rL /usr/lib/jvm/java-17-openjdk-amd64/ /jvm-resolved/

FROM scratch

COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /lib/x86_64-linux-gnu/libstdc++.so.6 /lib/x86_64-linux-gnu/libstdc++.so.6
COPY --from=build /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=build /usr/lib/x86_64-linux-gnu/libz.so.1 /usr/lib/x86_64-linux-gnu/libz.so.1
COPY --from=build /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=build /etc/ld.so.cache /etc/ld.so.cache

COPY --from=build /jvm-resolved/ /usr/lib/jvm/java-17-openjdk-amd64/
COPY --from=build /etc/ssl/certs/java/cacerts /etc/ssl/certs/java/cacerts

COPY --from=build /etc/java-17-openjdk/security/ /etc/java-17-openjdk/security/

COPY --from=build /src/target/spring-petclinic-3.3.0-SNAPSHOT.jar /usr/src/spring-petclinic-3.3.0-SNAPSHOT.jar
