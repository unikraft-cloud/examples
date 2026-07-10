FROM --platform=$BUILDPLATFORM node:24-bookworm

# Install sshd and other useful utilities
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        openssh-server vim jq rsync \
    && rm -rf /var/lib/apt/lists/*

# Install OpenClaw and the Unikraft Sandbox skill for OpenClaw
RUN npm i -g openclaw
RUN openclaw skills install unikraft-sandbox

COPY ./entrypoint.sh /usr/bin/entrypoint.sh
