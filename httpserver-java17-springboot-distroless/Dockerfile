FROM --platform=linux/x86_64 debian:bookworm AS build

RUN set -xe ; \
    apt -yqq update ; \
    apt -yqq install default-jre ; \
    apt -yqq install default-jdk; \
    apt -yqq install curl zip \
    ;

RUN ldconfig /usr/lib/jvm/java-17-openjdk-amd64/lib/

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

FROM gcr.io/distroless/java17-debian13

COPY --from=build /src/target/demo-0.0.1-SNAPSHOT.jar /usr/src/demo-0.0.1-SNAPSHOT.jar
