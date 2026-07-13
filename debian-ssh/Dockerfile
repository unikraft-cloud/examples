FROM --platform=linux/x86_64 debian:bookworm AS build

WORKDIR /src

RUN set -xe; \
    apt-get -yqq update; \
    apt-get -yqq install openssh-server strace net-tools \
    ;

RUN echo "root:unikraft" | chpasswd

RUN mkdir /run/sshd

COPY ./sshd_config /etc/ssh/sshd_config

COPY ./wrapper.sh /usr/bin/wrapper.sh
