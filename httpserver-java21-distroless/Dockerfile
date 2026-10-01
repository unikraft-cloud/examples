# --- Build Stage ---
FROM --platform=linux/x86_64 ubuntu:24.04 AS build

RUN set -xe ; \
    apt-get -yqq update ; \
    apt-get -yqq install openjdk-21-jdk openjdk-21-jre-headless \
    ;

WORKDIR /src
COPY ./SimpleHttpServer.java /src/SimpleHttpServer.java
RUN javac SimpleHttpServer.java

# --- Runtime Stage: distroless ---
FROM --platform=linux/x86_64 gcr.io/distroless/java21-debian13

COPY --from=build /src/SimpleHttpServer.class /usr/src/SimpleHttpServer.class
