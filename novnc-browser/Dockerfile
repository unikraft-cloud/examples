# The rootfs is a full Ubuntu desktop, so the main package install must run
# under the target architecture (emulated on ARM hosts): package maintainer
# scripts execute x86_64 binaries.  Everything that does not need target
# execution is kept out of that stage: noVNC/websockify are cloned natively
# (HTML/JS/Python only), and the Mozilla PPA is configured statically with a
# BuildKit-fetched key instead of add-apt-repository, which would drag the
# whole software-properties/python stack through the emulated build.
FROM --platform=$BUILDPLATFORM ubuntu:22.04 AS novnc-src

RUN apt-get update && \
    apt-get -y install --no-install-recommends git ca-certificates && \
    git clone --depth 1 --branch v1.5.0 https://github.com/novnc/noVNC.git /opt/noVNC && \
    git clone --depth 1 --branch v0.12.0 https://github.com/novnc/websockify /opt/noVNC/utils/websockify && \
    ln -s /opt/noVNC/vnc.html /opt/noVNC/index.html

FROM --platform=linux/x86_64 ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV DEBIAN_PRIORITY=high

# dpkg fsyncs after unpacking each file; under QEMU those syscalls dominate the
# emulated install time. This layer is ephemeral — only its installed files end
# up in the final rootfs — so disabling the fsyncs is safe and a sizeable win.
RUN echo 'force-unsafe-io' > /etc/dpkg/dpkg.cfg.d/02speedup

# Mozilla team PPA public signing key, vendored from
# https://api.launchpad.net/devel/~mozillateam/+archive/ubuntu/ppa?ws.op=getSigningKeyData
# (fingerprint 738BEB9321D1AAEC13EA9391AEBDF4819BE21867).  If the PPA ever
# rotates its key, apt fails signature verification until this file is
# refreshed from that endpoint.
COPY --chmod=644 mozillateam-ppa.asc /etc/apt/keyrings/mozillateam-ppa.asc

# ca-certificates first (from the plain-http archive): the PPA is served
# over https, and without the CA store apt-get update skips it silently.
RUN apt-get update && \
    apt-get -y install --no-install-recommends ca-certificates && \
    echo "deb [signed-by=/etc/apt/keyrings/mozillateam-ppa.asc] https://ppa.launchpadcontent.net/mozillateam/ppa/ubuntu jammy main" \
        > /etc/apt/sources.list.d/mozillateam-ppa.list && \
    apt-get update && \
    # --no-install-recommends keeps the emulated install lean: recommends for
    # the desktop packages (docs, help, icon themes, extra fonts, GNOME bits)
    # each drag in their own postinst/triggers under QEMU. Everything actually
    # needed at runtime is listed explicitly below, and firefox-esr is folded
    # into this one transaction so dpkg triggers run once instead of twice.
    apt-get -y install --no-install-recommends \
    # Core desktop: virtual X server, window manager, panel, VNC server
    xvfb \
    mutter \
    tint2 \
    x11vnc \
    # Invoked by image/*.sh: xdpyinfo (x11-utils) gates Xvfb readiness,
    # xdotool waits on windows, netstat (net-tools) checks the VNC port
    x11-utils \
    xdotool \
    net-tools \
    scrot \
    # Demo apps wired into the tint2 taskbar launchers
    xterm \
    gedit \
    xpaint \
    # Previously satisfied by recommends, now required explicitly: a session
    # bus for mutter/GTK apps, and base fonts so text isn't rendered as tofu
    dbus-x11 \
    fonts-dejavu-core \
    fonts-liberation \
    # The browser this example exists to demonstrate
    firefox-esr \
    # runs websockify; previously came in via software-properties-common
    python3 \
    && \
    rm -rf /var/lib/apt/lists/*

# Install noVNC (fetched natively above; needs no target toolchain)
COPY --from=novnc-src /opt/noVNC /opt/noVNC

COPY ./image /

COPY --chmod=755 ./wrapper.sh /wrapper.sh

ENTRYPOINT [ "/wrapper.sh" ]
