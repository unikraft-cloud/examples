# Umami Web Analytics

This guide shows you how to deploy [Umami](https://umami.is), an open-source, privacy-focused web analytics platform.

Umami requires PostgreSQL.
This example deploys the [postgres](../postgres/) example as the database backend and runs Umami as a Next.js standalone application.

To run it, follow these steps:

1. Install the CLI and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/umami/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/umami/
```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

or

```bash title="kraft"
# Set Unikraft Cloud access token
export UKC_TOKEN=token
# Set metro to Frankfurt, DE
export UKC_METRO=fra
```

## Step 1: Deploy PostgreSQL

First, deploy a PostgreSQL instance using the [postgres](../postgres/) example:

```bash title="unikraft"
cd ../postgres/
unikraft build . --output <my-org>/postgres:latest
unikraft run --metro=fra -p 5432:5432/tls -m 1536M -e POSTGRES_PASSWORD=<password> -e POSTGRES_DB=umami --scale-to-zero=off <my-org>/postgres:latest
```

or

```bash title="kraft"
cd ../postgres/
kraft cloud deploy -p 5432:5432/tls -M 1G -e POSTGRES_PASSWORD=<password> -e POSTGRES_DB=umami --scale-to-zero off .
```

Note the service FQDN from the output (e.g., `young-thunder-fbafrsxj.fra.unikraft.app`).

## Step 2: Run Database Migrations

Umami requires database tables to be created before first use.
Run migrations from your local machine using the Prisma CLI:

```bash
# Clone Umami locally (only needed for the Prisma schema and migrations)
git clone --depth 1 --branch v3.0.3 https://github.com/umami-software/umami.git /tmp/umami-migrate
cd /tmp/umami-migrate

# Install dependencies
npm install -g pnpm && pnpm install --frozen-lockfile

# Patch pgcrypto (not available in the Unikraft postgres image, not needed on PG16+)
# On macOS, use: sed -i '' 's/...' instead
sed -i 's/CREATE EXTENSION IF NOT EXISTS "pgcrypto";/-- pgcrypto: not needed on PG16+/' \
    prisma/migrations/01_init/migration.sql

# Run migrations
DATABASE_URL="postgresql://postgres:<password>@<postgres-fqdn>:5432/umami?sslmode=require" \
  npx prisma migrate deploy
```

> **Note:** Use `?sslmode=require` when connecting over the public FQDN.

## Step 3: Deploy Umami

Return to the `umami/` example directory and deploy:

```bash title="unikraft"
cd ../umami/
unikraft build . --output <my-org>/umami:latest
unikraft run --metro=fra \
  -p 443:3000/tls+http \
  -m 1536M \
  -e DATABASE_URL="postgresql://postgres:<password>@<postgres-fqdn>:5432/umami?sslmode=require" \
  -e APP_SECRET="$(openssl rand -hex 32)" \
  -e DISABLE_TELEMETRY=1 \
  <my-org>/umami:latest
```

or

```bash title="kraft"
cd ../umami/
kraft cloud deploy \
  -p 443:3000 \
  -M 1536 \
  -e DATABASE_URL="postgresql://postgres:<password>@<postgres-fqdn>:5432/umami?sslmode=require" \
  -e APP_SECRET="$(openssl rand -hex 32)" \
  -e DISABLE_TELEMETRY=1 \
  .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: umami-f7k2x
 ├────────── uuid: c742ae33-d502-481c-b691-7732f00abf0c
 ├───────── state: starting
 ├──────── domain: https://blue-bush-59v2y072.fra.unikraft.app
 ├───────── image: umami@sha256:d7f3221eee2ecbd8d90fcebe97eb7dc7f5989ee95c4cedd4a9fe728a709890b0
 ├──────── memory: 1536 MiB
 ├─────── service: blue-bush-59v2y072
 ├── private fqdn: umami-f7k2x.internal
 ├──── private ip: 10.0.8.193
 └────────── args: /usr/bin/node /app/server.js
```

Open the URL in a browser and log in with the default credentials:

| Username | Password |
|----------|----------|
| `admin`  | `umami`  |

**Change the default password immediately after first login.**

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `APP_SECRET` | Recommended | Secret for session encryption. Auto-generated if not set, but won't persist across restarts. |
| `DISABLE_TELEMETRY` | No | Set to `1` to disable Umami's telemetry |
| `COLLECT_API_ENDPOINT` | No | Custom tracker endpoint path (replaces `/api/send`) |

## Upgrading

To upgrade to a new Umami release:

1. Update `UMAMI_VERSION` in the `Dockerfile` (e.g., `v3.0.3` to `v3.1.0`)
2. Run database migrations again (Step 2) with the new version
3. Redeploy (Step 3)

Migrations are idempotent; already-applied migrations are skipped.

## Notes

- **Image size**: The `FROM scratch` image is ~386 MB (including GeoIP data for visitor location tracking). Umami requires at least 1536 MiB of memory to unpack the initramfs and run. To reduce the image by ~54 MB (and lower the minimum memory to 1024 MiB), add `rm -rf /app/.next/standalone/geo` to the `Dockerfile` build stage. This disables visitor location tracking.
- **pgcrypto**: The Unikraft Cloud postgres example does not include the `pgcrypto` extension. This is not a problem because PostgreSQL 16+ provides `gen_random_uuid()` as a built-in function. The migration patch in Step 2 and in the `Dockerfile` comments out the `CREATE EXTENSION` statement.

## Cleanup

```bash title="unikraft"
unikraft instances delete <umami-instance>
unikraft instances delete <postgres-instance>
```

or

```bash title="kraft"
kraft cloud instance remove <umami-instance>
kraft cloud instance remove <postgres-instance>
```

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

or

```bash title="kraft"
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft) or the [legacy CLI Reference](https://unikraft.com/docs/cli/kraft/overview).
