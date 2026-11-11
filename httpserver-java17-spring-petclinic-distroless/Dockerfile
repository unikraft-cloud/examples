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

FROM gcr.io/distroless/java17-debian13

COPY --from=build /src/target/spring-petclinic-3.3.0-SNAPSHOT.jar /usr/src/spring-petclinic-3.3.0-SNAPSHOT.jar
