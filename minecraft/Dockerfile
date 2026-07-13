FROM --platform=linux/x86_64 itzg/minecraft-server:java25

RUN set -xe; \
    apt-get -yqq update; \
    apt-get -yqq install openssh-server \
    ;

RUN ssh-keygen -A

COPY sshd_config /etc/ssh/sshd_config

RUN mkdir -p /run/sshd

COPY --chmod=755 wrapper.sh /wrapper.sh

# Patch startup scripts to create a Unikraft Cloud template snapshot right
# before the Java server process starts (i.e., before world generation).
COPY --chmod=755 patches/start-configuration /image/scripts/start-configuration
COPY --chmod=755 patches/start-finalExec /image/scripts/start-finalExec
