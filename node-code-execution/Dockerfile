# Install dependencies natively on the build host — they are pure JavaScript.
FROM --platform=$BUILDPLATFORM node:25-slim AS build

WORKDIR /src

COPY package*.json ./
RUN npm install --omit=dev

# Target-architecture runtime image (copy-only, nothing runs under emulation).
FROM --platform=linux/x86_64 node:25-slim

WORKDIR /src

# Bring over the package manifests and node_modules together — npm doesn't
# create node_modules when there is nothing to install, so copying it by name
# would fail.
COPY --from=build /src/ ./

COPY ./server.ts ./
COPY ./wrapper.sh /wrapper.sh
