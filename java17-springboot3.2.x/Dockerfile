FROM  --platform=linux/x86_64 debian:bookworm AS build

RUN set -xe ; \
    apt -yqq update ; \
    apt -yqq install default-jre default-jdk curl unzip ;

RUN ldconfig /usr/lib/jvm/java-17-openjdk-amd64/lib/

WORKDIR /src

RUN set -xe ; \
    curl -G https://start.spring.io/starter.zip \
         -d applicationName=DemoApplication \
         -d artifactId=demo \
         -d bootVersion=3.2.2 \
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

RUN set -xe ; \
    mkdir /tmpdir

FROM scratch

COPY --from=build /tmpdir /tmp
COPY --from=build /src/target/demo-0.0.1-SNAPSHOT.jar /usr/src/demo-0.0.1-SNAPSHOT.jar
