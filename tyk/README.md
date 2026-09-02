# API Gateways: Tyk

An API gateway is the entry point to your services, handling authentication, routing, rate-limiting, and observability at the edge of your infrastructure.
API traffic fluctuates, so a gateway that scales to zero when idle and starts in milliseconds when traffic returns keeps your API edge ready without paying for it overnight.

This example uses [`Tyk`](https://tyk.io/), an API gateway and management platform.
Tyk is used together with Redis to store API tokens and OAuth clients.

To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/tyk/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/tyk/
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

## Redis

The `REDIS_PASSWORD` environment variable sets the Redis `requirepass` directive.
If not provided, it defaults to `unikraft`.
Build and deploy the Redis instance (used internally by Tyk):

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft build ./redis --output <my-org>/redis:latest
unikraft run --metro fra \
  -m 256M \
  --scale-to-zero policy=idle,cooldown-time=1000,stateful=true \
  --domain tyk-redis.internal \
  -e REDIS_PASSWORD=unikraft \
  --image <my-org>/redis:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy \
  -M 256Mi \
  --scale-to-zero idle \
  --scale-to-zero-stateful \
  --scale-to-zero-cooldown 1s \
  --domain tyk-redis.internal \
  --env REDIS_PASSWORD=unikraft \
  ./redis/
```

Make sure to replace `<my-org>` with your username / org-name in the unikraft CLI commands above.

The output shows the Redis instance details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:           fra
name:            redis-6vgvc
uuid:            63b86d17-06ca-4f95-b921-56e5b3245554
state:           starting
image:           <my-org>/redis
resources:
  memory:        256MiB
  vcpus:         1
service:
  name:          snowy-water-wivk1i4r
  uuid:          6612de91-d639-4b5a-95d1-b7ae6e91e3c1
  domains:
  - fqdn:        tyk-redis.internal
networks:
- uuid:          19e4b80a-9501-448d-99a6-ec3f7b90805e
  private-ip:    10.0.0.29
  mac:           12:b0:0a:00:01:49
timestamps:
  created:       just now
scale-to-zero:
  enabled:       true
  policy:        idle
  stateful:      true
  cooldown-time: 1s
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: redis-6vgvc
 ├───────── uuid: 63b86d17-06ca-4f95-b921-56e5b3245554
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: tyk-redis.internal
 ├──────── image: oci://unikraft.io/<my-org>/redis@sha256:933b8b7714924eb2de880e0f32792698b14a13c83d5aee0f52dddcab5c97099d
 ├─────── memory: 256 MiB
 ├────── service: snowy-water-wivk1i4r
 ├─ private fqdn: redis-6vgvc.internal
 └─── private ip: 10.0.0.29
```

## Tyk

Build and deploy the Tyk instance.
Set `TYK_GW_STORAGE_HOST` to the same internal domain you assigned to the Redis instance (`tyk-redis.internal` in this guide).
If `TYK_GW_STORAGE_HOST` is unset, Tyk tries to connect to a Redis instance at `tyk-redis.internal` by default.

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft build ./tyk --output <my-org>/tyk:latest
unikraft run --metro fra \
  -m 256M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  -e TYK_GW_STORAGE_PASSWORD=unikraft \
  -e TYK_GW_STORAGE_HOST=tyk-redis.internal \
  --image <my-org>/tyk:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy \
  -M 256Mi \
  -p 443:8080/tls+http \
  --scale-to-zero on \
  --scale-to-zero-cooldown 1s \
  --env TYK_GW_STORAGE_PASSWORD=unikraft \
  --env TYK_GW_STORAGE_HOST=tyk-redis.internal \
  ./tyk/
```

Make sure to replace `<my-org>` with your username / org-name in the unikraft CLI commands above.

The output shows the Tyk instance details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         tyk-s9ixd
uuid:         4e8a5e56-2d0b-4ca4-88b4-aa816129a66d
state:        starting
image:        <my-org>/tyk
resources:
  memory:     256MiB
  vcpus:      1
service:
  name:       icy-haze-8ph4u8cz
  uuid:       89079646-353a-4a19-99ac-5498c7d626ad
  domains:
  - fqdn:     icy-haze-8ph4u8cz.fra.unikraft.app
networks:
- uuid:       8085804f-0fe0-4847-ad6e-8518edba126e
  private-ip: 10.0.0.1
  mac:        12:b0:0a:00:0e:b1
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: tyk-s9ixd
 ├───────── uuid: 4e8a5e56-2d0b-4ca4-88b4-aa816129a66d
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://icy-haze-8ph4u8cz.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/tyk@sha256:4954033ada90f980f279e5d825dd7971111a429578ce38be764893ba0d1f358d
 ├─────── memory: 256 MiB
 ├────── service: icy-haze-8ph4u8cz
 ├─ private fqdn: tyk-s9ixd.internal
 └─── private ip: 10.0.0.1
```

In this case, the instance names are `redis-6vgvc` and `tyk-s9ixd`, and the Tyk address is `https://icy-haze-8ph4u8cz.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Tyk instance on Unikraft Cloud:

```bash
curl https://icy-haze-8ph4u8cz.fra.unikraft.app/hello
```

```text
{"status":"pass","version":"v5.3.0-dev","description":"Tyk GW","details":{"redis":{"status":"pass","componentType":"datastore","time":"2026-05-25T12:26:07Z"}}}
```

You can list information about the instances by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME         STATE   IMAGE           MEMORY  VCPUS  FQDN                                CREATED
fra    tyk-s9ixd    standby <my-org>/tyk    256MiB  1      icy-haze-8ph4u8cz.fra.unikraft.app  just now
fra    redis-6vgvc  running <my-org>/redis  256MiB  1      tyk-redis.internal                  1 minute ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME         FQDN                                STATE    STATUS      IMAGE                                             MEMORY   VCPUS  ARGS  BOOT TIME
tyk-s9ixd    icy-haze-8ph4u8cz.fra.unikraft.app  standby  standby     oci://unikraft.io/<my-org>/tyk@sha256:4954033...  256 MiB  1            158.32 ms
redis-6vgvc  tyk-redis.internal                  running  since 1min  oci://unikraft.io/<my-org>/redis@sha256:933b8...  256 MiB  1            1811.99 ms
```

When done, you can remove the instances:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete redis-6vgvc tyk-s9ixd
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove redis-6vgvc tyk-s9ixd
```

## Customize your app

To customize the Tyk app, you can update:

* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile` / `rootfs/`: the Tyk filesystem (in this case the configuration file `/etc/tyk.conf`)

It's unlikely you will have to update the `Kraftfile` specification.

Update the contents of the `rootfs/etc/tyk.conf` file for a different configuration.

You can also update the `Dockerfile` in order to extend the Tyk filesystem with extra data files or configuration files.

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
