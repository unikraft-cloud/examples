FROM alpine:3.22 AS novnc

RUN apk add --no-cache git && \
    git clone --depth 1 --branch v1.5.0 https://github.com/novnc/noVNC.git /opt/noVNC && \
    git clone --depth 1 --branch v0.12.0 https://github.com/novnc/websockify /opt/noVNC/utils/websockify && \
    rm -rf /opt/noVNC/.git /opt/noVNC/utils/websockify/.git && \
    ln -s vnc.html /opt/noVNC/index.html

FROM debian:13-slim

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    xvfb \
    x11-utils \
    xdotool \
    openbox \
    lxpanel \
    xterm \
    x11vnc \
    net-tools \
    python3 \
    adwaita-icon-theme \
    fonts-dejavu-core \
    ca-certificates \
    firefox-esr && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/* /var/log/* \
    /usr/share/doc /usr/share/man /usr/share/info

COPY --from=novnc /opt/noVNC /opt/noVNC

COPY ./image /

COPY --chmod=755 ./wrapper.sh /opt/novnc/wrapper.sh

ENTRYPOINT [ "/opt/novnc/wrapper.sh" ]
