FROM  --platform=linux/x86_64 debian:bookworm AS build

RUN set -xe ; \
    apt -yqq update ; \
        apt -yqq install default-jre ; \
        apt -yqq install default-jdk \
    ;

RUN ldconfig /usr/lib/jvm/java-17-openjdk-amd64/lib/

WORKDIR /src

COPY ./SimpleHttpServer.java /src/SimpleHttpServer.java

RUN javac SimpleHttpServer.java

FROM scratch

COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /lib/x86_64-linux-gnu/libstdc++.so.6 /lib/x86_64-linux-gnu/libstdc++.so.6
COPY --from=build /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=build /usr/lib/x86_64-linux-gnu/libz.so.1 /usr/lib/x86_64-linux-gnu/libz.so.1
COPY --from=build /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=build /etc/ld.so.cache /etc/ld.so.cache

COPY --from=build /usr/lib/jvm/java-17-openjdk-amd64/ /usr/lib/jvm/java-17-openjdk-amd64/

COPY --from=build /etc/java-17-openjdk/security/ /etc/java-17-openjdk/security/

COPY --from=build /src/SimpleHttpServer.class /usr/src/SimpleHttpServer.class
