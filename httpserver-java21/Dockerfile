# --- Build Stage ---
# Use Ubuntu 24.04 as the base image (includes Java 21 in official repos)
FROM --platform=$BUILDPLATFORM ubuntu:24.04 AS build

# 1. Install OpenJDK 21
RUN set -xe ; \
    apt-get -yqq update ; \
    apt-get -yqq install openjdk-21-jdk openjdk-21-jre-headless \
    ;

# 2. Re-generate ldconfig for Java 21
# Note: Ensure the path matches the Ubuntu directory structure
RUN ldconfig /usr/lib/jvm/java-21-openjdk-amd64/lib/server/

WORKDIR /src

COPY ./SimpleHttpServer.java /src/SimpleHttpServer.java

RUN javac SimpleHttpServer.java

# --- Runtime Stage (minimal) ---
FROM --platform=$BUILDPLATFORM scratch

# --- Copy system libraries (glibc, libz, etc.) ---
# These paths are standard for Ubuntu/Debian x86_64

COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /lib/x86_64-linux-gnu/libstdc++.so.6 /lib/x86_64-linux-gnu/libstdc++.so.6
COPY --from=build /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=build /usr/lib/x86_64-linux-gnu/libz.so.1 /usr/lib/x86_64-linux-gnu/libz.so.1
COPY --from=build /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=build /etc/ld.so.cache /etc/ld.so.cache

# --- Copy Java 21 Runtime ---
COPY --from=build /usr/lib/jvm/java-21-openjdk-amd64/ /usr/lib/jvm/java-21-openjdk-amd64/
COPY --from=build /etc/ssl/certs/java/cacerts /etc/ssl/certs/java/cacerts
COPY --from=build /etc/java-21-openjdk/security/ /etc/java-21-openjdk/security/

# --- Copy the compiled application ---
COPY --from=build /src/SimpleHttpServer.class /usr/src/SimpleHttpServer.class
