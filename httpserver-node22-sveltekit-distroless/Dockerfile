FROM node:22-bookworm AS base

WORKDIR /app

COPY package.json /app

RUN npm install

FROM base AS build

COPY . /app

RUN npm run build; \
    npm prune --production

RUN <<EOF cat >> /app/build/package.json
{"type": "module"}
EOF


FROM gcr.io/distroless/nodejs22-debian13:nonroot

# Svelte
COPY --from=build /app/build /app/build
COPY --from=build /app/node_modules /app/node_modules
