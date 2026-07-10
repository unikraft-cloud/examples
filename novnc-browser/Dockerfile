FROM --platform=$BUILDPLATFORM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV DEBIAN_PRIORITY=high

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install \
    xvfb \
    xterm \
    xdotool \
    scrot \
    imagemagick \
    mutter \
    x11vnc \
    tint2 \
    git \
    net-tools \
    gedit \
    x11-apps \
    xpaint \
    software-properties-common

# Install Firefox ESR
RUN add-apt-repository ppa:mozillateam/ppa && \
    apt-get install -y --no-install-recommends \
    firefox-esr

# Install noVNC
RUN git clone --branch v1.5.0 https://github.com/novnc/noVNC.git /opt/noVNC && \
    git clone --branch v0.12.0 https://github.com/novnc/websockify /opt/noVNC/utils/websockify && \
    ln -s /opt/noVNC/vnc.html /opt/noVNC/index.html

COPY ./image /

COPY --chmod=755 ./wrapper.sh /wrapper.sh

ENTRYPOINT [ "/wrapper.sh" ]
