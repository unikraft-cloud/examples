FROM node:24-bookworm

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        openssh-server vim jq rsync \
    && rm -rf /var/lib/apt/lists/*

COPY package.json package-lock.json /opt/openclaw/

RUN npm ci --omit=dev --prefix /opt/openclaw \
    && npm cache clean --force \
    && ln -s /opt/openclaw/node_modules/.bin/openclaw /usr/local/bin/openclaw

COPY ./entrypoint.sh /usr/bin/entrypoint.sh
