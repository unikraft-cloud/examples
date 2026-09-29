# Phoenix with PostgreSQL

[Phoenix](https://phoenixframework.org/) is a web development framework written in Elixir, designed for building scalable and maintainable applications. This example demonstrates how to deploy a Phoenix application with a PostgreSQL database on [Unikraft Cloud](https://unikraft.cloud/).

This example app has been generated using [Phoenix Express](https://hexdocs.pm/phoenix/up_and_running.html#phoenix-express), and the Dockerfile
used for building the rootfs was generated following the instructions [here](https://hexdocs.pm/phoenix/releases.html).

To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/phoenix-postgres` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/phoenix-postgres/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

## PostgreSQL

Create a volume for PostgreSQL data persistence:

```bash title="unikraft"
unikraft volume create --metro fra --name db-data --size 512M
```

You can list the created volume by running:

```bash title="unikraft"
unikraft volume list
```

```ansi title="unikraft"
METRO  NAME     STATE      SIZE    CREATED
fra    db-data  available  512MiB  just now
```

Update `POSTGRES_PASSWORD` with a secure password and build and deploy the PostgreSQL instance:

```bash title="unikraft"
unikraft build ./postgres --output <my-org>/postgres:latest
unikraft run --metro fra \
  -m 2G \
  --scale-to-zero policy=idle,cooldown-time=1000,stateful=true \
  --domain postgres.internal \
  --env POSTGRES_USER=postgres \
  --env POSTGRES_PASSWORD=example_123 \
  --env POSTGRES_DB=myapp_prod \
  --env PGDATA=/var/lib/postgresql/data/pgdata \
  --volume db-data:/var/lib/postgresql/data \
  --image <my-org>/postgres:latest
```

Make sure to replace `<my-org>` with your username / org-name.

The output shows the PostgreSQL instance details:

```ansi title="unikraft"
metro:                 fra
name:                  postgres-ik5at
uuid:                  3776dbfe-2937-45e7-8079-c54275ef3cff
state:                 starting
image:                 <my-org>/postgres
runtime:
  env:
    PGDATA:            /var/lib/postgresql/data/pgdata
    POSTGRES_DB:       myapp_prod
    POSTGRES_PASSWORD: *
    POSTGRES_USER:     postgres
resources:
  memory:              2GiB
  vcpus:               1
service:
  name:                dry-cloud-q8u7yjkl
  uuid:                cf364e60-46b0-4031-bace-296fa8e24ac4
  domains:
  - fqdn:              postgres.internal
volumes:
- name:                db-data
  uuid:                0efda5f6-21d2-48c7-84f5-8efe87e33090
  at:                  /var/lib/postgresql/data
networks:
- uuid:                cab79d9f-08a8-4741-8efd-58d9a1faa35d
  private-ip:          10.0.14.117
  mac:                 12:b0:0a:00:0e:75
timestamps:
  created:             just now
scale-to-zero:
  enabled:             true
  policy:              idle
  stateful:            true
  cooldown-time:       1s
```

## Phoenix

Generate a secret key for Phoenix:

```bash
openssl rand -base64 48
```

Replace `<your-secret-key-base>` in the commands below with the generated value, and update the password in `DATABASE_URL` to match the one set for PostgreSQL.
Then, deploy the Phoenix instance:

```bash title="unikraft"
unikraft build ./phoenix --output <my-org>/phoenix:latest
unikraft run --metro fra \
  -m 2G \
  -p 443:4000/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --env SECRET_KEY_BASE=<your-secret-key-base> \
  --env DATABASE_URL=ecto://postgres:example_123@postgres.internal:5432/myapp_prod \
  --image <my-org>/phoenix:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:               fra
name:                phoenix-hd29m
uuid:                fa4db9cf-f7b5-4b8b-b007-8fd1ce87c7e1
state:               starting
image:               <my-org>/phoenix
runtime:
  env:
    DATABASE_URL:    ecto://postgres:example_123@postgres.internal:5432/myapp_prod
    SECRET_KEY_BASE: <your-secret-key-base>
resources:
  memory:            2GiB
  vcpus:             1
service:
  name:              wild-moon-pkwsqc49
  uuid:              1d1b8732-d2d5-41ab-ab8f-1b19fc27c14d
  domains:
  - fqdn:            wild-moon-pkwsqc49.fra.unikraft.app
networks:
- uuid:              d14f07de-1c81-4309-bbf3-ab8ab6aeefe6
  private-ip:        10.0.14.53
  mac:               12:b0:0a:00:0e:35
timestamps:
  created:           just now
scale-to-zero:
  enabled:           true
  policy:            on
  cooldown-time:     1s
```

In this case, the instance names are `postgres-ik5at` and `phoenix-hd29m`.
They're different for each run.

Use a browser to access the Phoenix application using the URL from the `fqdn` field in the output.

You can list information about the instances by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME            STATE    IMAGE              MEMORY  VCPUS  FQDN                                 CREATED
fra    phoenix-hd29m   running  <my-org>/phoenix   2GiB    1      wild-moon-pkwsqc49.fra.unikraft.app  just now
fra    postgres-ik5at  standby  <my-org>/postgres  2GiB    1      postgres.internal                    3 minutes ago
```

When done, you can remove the instances:

```bash title="unikraft"
unikraft instances delete postgres-ik5at phoenix-hd29m
```

## Volume

This deployment creates a volume (`db-data`) for PostgreSQL data persistence.
The volume persists after removing instances, allowing you to redeploy without losing data.
To remove the volume:

```bash title="unikraft"
unikraft volume delete db-data
```

## Learn more

- [Phoenix's Documentation](https://hexdocs.pm/phoenix/)
- [PostgreSQL's Documentation](https://www.postgresql.org/docs/)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
