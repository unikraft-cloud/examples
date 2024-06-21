FROM --platform=$BUILDPLATFORM debian:bookworm AS build

RUN set -xe ; \
    apt -yqq update ; \
    apt -yqq install --no-install-recommends --no-install-suggests git default-jre default-jdk curl unzip \
    ;

RUN ldconfig /usr/lib/jvm/java-17-openjdk-amd64/lib/

RUN git clone https://github.com/spring-projects/spring-petclinic.git /src

WORKDIR /src

RUN --mount=type=cache,target=/root/.m2 ./mvnw package

RUN mkdir /tmpdir

FROM scratch

COPY --from=build /tmpdir /tmp
COPY --from=build /src/target/spring-petclinic-3.3.0-SNAPSHOT.jar /usr/src/spring-petclinic-3.3.0-SNAPSHOT.jar
