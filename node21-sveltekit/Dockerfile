FROM node:21-alpine AS deps

WORKDIR /app

COPY package.json /app

RUN npm install -D @sveltejs/adapter-node
RUN npm install

FROM deps AS build

COPY . /app

RUN npm run build; \
    npm prune --production

RUN <<EOF cat >> /app/build/package.json
{"type": "module"}
EOF

FROM scratch AS prod

COPY --from=build /app/build /app/build
COPY --from=build /app/node_modules /app/node_modules
