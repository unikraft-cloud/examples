FROM node:24-bookworm

# Install sshd and other useful utilities
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        openssh-server vim jq rsync \
    && rm -rf /var/lib/apt/lists/*

# Install OpenClaw and the Unikraft Sandbox skill for OpenClaw.
# ClawHub flags the skill as "suspicious" (broad tool-use surface — expected
# for a sandbox-management skill, see
# https://clawhub.ai/procub3r/skills/unikraft-sandbox/security-audit), which
# makes non-interactive installs abort unless the risk is acknowledged.
RUN npm i -g openclaw
RUN openclaw skills install unikraft-sandbox --acknowledge-clawhub-risk

COPY ./entrypoint.sh /usr/bin/entrypoint.sh
