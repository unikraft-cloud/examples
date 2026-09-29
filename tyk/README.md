# API Gateways: Tyk

An API gateway is the entry point to your services, handling authentication, routing, rate-limiting, and observability at the edge of your infrastructure.
API traffic fluctuates, so a gateway that scales to zero when idle and starts in milliseconds when traffic returns keeps your API edge ready without paying for it overnight.

This example uses [`Tyk`](https://tyk.io/), an API gateway and management platform.
Tyk is used together with Redis to store API tokens and OAuth clients.

To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/tyk/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/tyk/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

## Redis

The `REDIS_PASSWORD` environment variable sets the Redis `requirepass` directive.
If not provided, it defaults to `unikraft`.
Build and deploy the Redis instance (used internally by Tyk):

```bash title="unikraft"
unikraft build ./redis --output <my-org>/redis:latest
unikraft run --metro fra \
  -m 256M \
  --scale-to-zero policy=idle,cooldown-time=1000,stateful=true \
  --domain tyk-redis.internal \
  -e REDIS_PASSWORD=unikraft \
  --image <my-org>/redis:latest
```

Make sure to replace `<my-org>` with your username / org-name in the unikraft CLI commands above.

The output shows the Redis instance details:

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

## Tyk

Build and deploy the Tyk instance.
Set `TYK_GW_STORAGE_HOST` to the same internal domain you assigned to the Redis instance (`tyk-redis.internal` in this guide).
If `TYK_GW_STORAGE_HOST` is unset, Tyk tries to connect to a Redis instance at `tyk-redis.internal` by default.

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

Make sure to replace `<my-org>` with your username / org-name in the unikraft CLI commands above.

The output shows the Tyk instance details:

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

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME         STATE   IMAGE           MEMORY  VCPUS  FQDN                                CREATED
fra    tyk-s9ixd    standby <my-org>/tyk    256MiB  1      icy-haze-8ph4u8cz.fra.unikraft.app  just now
fra    redis-6vgvc  running <my-org>/redis  256MiB  1      tyk-redis.internal                  1 minute ago
```

When done, you can remove the instances:

```bash title="unikraft"
unikraft instances delete redis-6vgvc tyk-s9ixd
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

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
