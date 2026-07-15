FROM node:24-bookworm

# Install sshd and other useful utilities
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        openssh-server vim jq rsync \
    && rm -rf /var/lib/apt/lists/*

# Install OpenClaw
RUN npm i -g openclaw

COPY ./entrypoint.sh /usr/bin/entrypoint.sh
