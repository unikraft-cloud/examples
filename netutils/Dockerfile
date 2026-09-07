FROM alpine:latest
WORKDIR /

RUN set -xe; \
    apk update; \
    apk add --no-cache \
        socat \
        dropbear \
        tcpdump \
        iputils \
        traceroute \
        bind-tools \
        socat

RUN echo "root:unikraft" | chpasswd

COPY ./motd /etc/motd
COPY ./profile /etc/profile

RUN mkdir -p /opt/unikraft
COPY ./dropbeard.sh /opt/unikraft/dropbeard.sh
