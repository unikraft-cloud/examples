FROM node:22-alpine AS build

RUN apk add --no-cache libc6-compat git binutils

WORKDIR /app

# Clone pinned Umami release
ARG UMAMI_VERSION=v3.0.3
RUN git clone --depth 1 --branch ${UMAMI_VERSION} https://github.com/umami-software/umami.git .

# Install pnpm and dependencies
RUN npm install -g pnpm && pnpm install --frozen-lockfile

# Copy Docker-specific middleware (disables auth middleware for container use)
RUN cp docker/middleware.ts src/middleware.ts

# The Unikraft Cloud postgres example does not include the pgcrypto extension.
# PG16+ has gen_random_uuid() built-in, so the extension is not needed.
RUN sed -i 's/CREATE EXTENSION IF NOT EXISTS "pgcrypto";/-- pgcrypto: not needed on PG16+/' \
    prisma/migrations/01_init/migration.sql

# Dummy DATABASE_URL required for prisma generate during build
ENV DATABASE_URL="postgresql://user:pass@localhost:5432/umami"
ENV NEXT_TELEMETRY_DISABLED=1

# Build: prisma client + tracker + geo database + Next.js app
RUN pnpm build-docker

# Strip node binary (~20 MB savings) and remove GeoIP data (~54 MB savings)
RUN strip /usr/local/bin/node && rm -rf /app/.next/standalone/geo

FROM scratch

# Node binary (stripped)
COPY --from=build /usr/local/bin/node /usr/bin/node

# System libraries
COPY --from=build /lib/ld-musl-x86_64.so.1 /lib/ld-musl-x86_64.so.1
COPY --from=build /usr/lib/libgcc_s.so.1 /usr/lib/libgcc_s.so.1
COPY --from=build /usr/lib/libstdc++.so.6 /usr/lib/libstdc++.so.6

# SSL certificates (needed for TLS database connections)
COPY --from=build /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

# Distribution configuration
COPY --from=build /etc/os-release /etc/os-release

# Next.js standalone output
COPY --from=build /app/.next/standalone /app/
COPY --from=build /app/.next/static /app/.next/static
COPY --from=build /app/public /app/public

ENV HOSTNAME=0.0.0.0
ENV PORT=3000
