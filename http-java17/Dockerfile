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

COPY --from=build /src/SimpleHttpServer.class /usr/src/SimpleHttpServer.class
