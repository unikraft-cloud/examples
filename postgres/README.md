# Serverless Databases: PostgreSQL

Serverless databases scale up the moment a query arrives and cost nothing while idle, instead of keeping a provisioned instance running around the clock.

This guide shows you how to use [PostgreSQL](https://www.postgresql.org/), a powerful, open source object-relational database system, in exactly that fashion.
The database runs in a lightweight virtual machine that scales to zero when not in use and resumes in milliseconds on the next connection.

To run it, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/postgres/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/postgres/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft login
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
# Set Unikraft Cloud access token
export UKC_TOKEN=token
# Set metro to Frankfurt, DE
export UKC_METRO=fra
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft build . --output <my-org>/postgres:latest
unikraft run --metro fra \
  -m 1G \
  -p 5432:5432/tls \
  --scale-to-zero policy=idle,cooldown-time=1000,stateful=true \
  -e POSTGRES_PASSWORD=unikraft \
  --image <my-org>/postgres:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy \
  -M 1Gi \
  -p 5432:5432/tls \
  --scale-to-zero idle \
  --scale-to-zero-stateful \
  --scale-to-zero-cooldown 1s \
  -e POSTGRES_PASSWORD=unikraft \
  .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         postgres-saan9
uuid:         3a1371f2-68c6-4187-84f8-c080f2b028ca
state:        starting
image:        <my-org>/postgres
resources:
  memory:     1024MiB
  vcpus:      1
service:
  uuid:       8e9d810b-b1da-a30b-fd42-5c30c1900cb5
  name:       young-thunder-fbafrsxj
  domains:
  - fqdn:     young-thunder-fbafrsxj.fra.unikraft.app
networks:
- uuid:       f1fab4c9-7951-75e3-ea1c-d87e47b4c9e2
  private-ip: 10.0.3.1
  mac:        12:b0:31:34:b1:96
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: postgres-saan9
 ├───────── uuid: 3a1371f2-68c6-4187-84f8-c080f2b028ca
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://young-thunder-fbafrsxj.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/postgres@sha256:2476c0373d663d7604def7c35ffcb4ed4de8ab231309b4f20104b84f31570766
 ├─────── memory: 1024 MiB
 ├────── service: young-thunder-fbafrsxj
 ├─ private fqdn: postgres-saan9.internal
 └─── private ip: 10.0.3.1
```

In this case, the instance name is `postgres-saan9` and the service `young-thunder-fbafrsxj`.
They're different for each run.

If you use port 5432/tls per the example above, you can now directly connect to postgres:

```console
psql -U postgres -h young-thunder-fbafrsxj.fra.unikraft.app
```

Use the `unikraft` password at the password prompt.
You should see output like:

```ansi
Password for user postgres:
psql (15.5 (Ubuntu 15.5-0ubuntu0.23.04.1), server 16.2)
WARNING: psql major version 15, server major version 16.
         Some psql features might not work.
Type "help" for help.

postgres=#
```

Use SQL and `psql` commands for your work.

> **Tip:**
> This example uses the [`idle` scale-to-zero policy](https://unikraft.com/docs/api/platform/v1/instances#scaletozero_policy) by default.
> It means that the instance will scale-to-zero even in the presence of `psql` connections.
>
> The PostgreSQL example makes use of scale-to-zero app support.
> This ensures that the instance isn't put into standby even for long running queries (during which the connections are also idle).
> To this end, the example loads the [`pg_ukc_scaletozero`](https://github.com/unikraft-cloud/pg_ukc_scaletozero) module into PostgreSQL, which suspends scale-to-zero during query processing.
> You can see this in action by running `SELECT pg_sleep(10);` and verifying that the instance keeps on running.

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME            STATE    IMAGE              ARGS  MEMORY  VCPUS  FQDN                                     CREATED
fra    postgres-saan9  running  <my-org>/postgres        1.0GiB  1      young-thunder-fbafrsxj.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME            FQDN                                     STATE    STATUS         IMAGE                                           MEMORY   VCPUS  ARGS  BOOT TIME
postgres-saan9  young-thunder-fbafrsxj.fra.unikraft.app  running  6 minutes ago  oci://unikraft.io/<my-org>/postgres@sha256:...  1.0 GiB  1            603.42 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instance remove postgres-saan9
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove postgres-saan9
```

## Using volumes

You can use [volumes](https://unikraft.com/docs/platform/volumes) for data persistence for your PostgreSQL instance.
For that you would first create a volume:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft volume create --set metro=fra --set name=postgres --set size=200M
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud volume create --name postgres --size 200Mi
```

Then start the PostgreSQL instance and mount that volume:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft build . --output <my-org>/postgres:latest
unikraft run --metro fra \
  -m 1G \
  -p 5432:5432/tls \
  --scale-to-zero policy=idle,cooldown-time=1000,stateful=true \
  -e POSTGRES_PASSWORD=unikraft \
  -e PGDATA=/volume/postgres \
  --volume postgres:/volume \
  --image <my-org>/postgres:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy \
  -M 1Gi \
  -p 5432:5432/tls \
  --scale-to-zero idle \
  --scale-to-zero-stateful \
  --scale-to-zero-cooldown 1s \
  -e POSTGRES_PASSWORD=unikraft \
  -e PGDATA=/volume/postgres \
  -v postgres:/volume \
  .
```

## Customize your deployment

Your deployment is a standard PostgreSQL installation.
Customizing the deployment means providing a different environment.

An obvious one is to use a different database password when starting PostgreSQL.
For that you use a different `POSTGRES_PASSWORD` environment variable when starting the PostgreSQL instance.

You could also use a different location to mount your volume or set extra configuration options.

You can use the PostgreSQL instance in conjunction with a frontend service, [see the guide here](https://unikraft.com/docs/platform/services).

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft --help
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft) or the [legacy CLI Reference](https://unikraft.com/docs/cli/kraft/overview).
