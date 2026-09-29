# Go and Redis HTTP Server

This guide explains how to create and deploy a Go app with a Redis database.
To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-go1.22-redis` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-go1.22-redis/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

## Redis

First, deploy the Redis instance.
Redis is an internal service (not publicly accessible), reached via the `go122-redis.internal` domain.
The Redis password is set at runtime via the `REDIS_PASSWORD` environment variable (defaults to `unikraft` if not provided).

```bash title="unikraft"
unikraft build ./redis --output <my-org>/httpserver-go-122-redis-db:latest
unikraft run --metro fra \
  -m 256M \
  --scale-to-zero policy=idle,cooldown-time=1000,stateful=true \
  --domain go122-redis.internal \
  -e REDIS_PASSWORD=unikraft \
  --image <my-org>/httpserver-go-122-redis-db:latest
```

Make sure to replace `<my-org>` with your username / org-name.

The output shows the Redis instance details:

```ansi title="unikraft"
metro:           fra
name:            httpserver-go-122-redis-db-2xc9u
uuid:            8abe24f6-5670-4e9b-8955-8ec10f3bad21
state:           starting
image:           <my-org>/httpserver-go-122-redis-db
resources:
  memory:        256MiB
  vcpus:         1
service:
  name:          late-sound-rhboe98o
  uuid:          01953c15-8a2e-4c1a-ac24-98a9417c5aa2
  domains:
  - fqdn:        go122-redis.internal
networks:
- uuid:          e76ae319-d210-4566-ad75-baed32fc3d2b
  private-ip:    10.0.0.85
  mac:           12:b0:0a:00:00:55
timestamps:
  created:       just now
scale-to-zero:
  enabled:       true
  policy:        idle
  stateful:      true
  cooldown-time: 1s
```

## Go HTTP Server

Next, deploy the Go HTTP server.
It connects to Redis using the `REDIS_ADDR` and `REDIS_PASS` environment variables:

```bash title="unikraft"
unikraft build ./httpserver-go --output <my-org>/httpserver-go-122-redis-app:latest
unikraft run --metro fra \
  -m 256M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --env REDIS_ADDR=go122-redis.internal:6379 \
  --env REDIS_PASS=unikraft \
  --image <my-org>/httpserver-go-122-redis-app:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:           fra
name:            httpserver-go-122-redis-app-bnnnc
uuid:            82093bcf-fc4c-471c-89c8-4d0b7810e280
state:           starting
image:           <my-org>/httpserver-go-122-redis-app
runtime:
  env:
    REDIS_ADDR:  go122-redis.internal:6379
    REDIS_PASS:  unikraft
resources:
  memory:        256MiB
  vcpus:         1
service:
  name:          frosty-cherry-32qs6na2
  uuid:          bcb9a2af-cfce-4731-9844-5a368696ee7d
  domains:
  - fqdn:        frosty-cherry-32qs6na2.fra.unikraft.app
networks:
- uuid:          f9030f74-4e85-445b-a57e-36ec76137c88
  private-ip:    10.0.0.173
  mac:           12:b0:0a:00:00:ad
timestamps:
  created:       just now
scale-to-zero:
  enabled:       true
  policy:        on
  cooldown-time: 1s
```

In this case, the instance names are `httpserver-go-122-redis-db-2xc9u` and `httpserver-go-122-redis-app-bnnnc`.
They're different for each run.

To set a value in Redis via the Go server, use the URL from the `fqdn` field:

```bash
curl -X POST -d "key=my-key" -d "value=my-value" https://<FQDN>
```

```
Success!
```

You can then retrieve the value:

```bash
curl https://<FQDN>/?key=my-key
```

```
Key "my-key" has value "my-value"
```

You can list information about the instances by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                               STATE    IMAGE                                 ARGS  MEMORY  VCPUS  FQDN                                     CREATED
fra    httpserver-go-122-redis-app-bnnnc  standby  <my-org>/httpserver-go-122-redis-app        256MiB  1      frosty-cherry-32qs6na2.fra.unikraft.app  4 minutes ago
fra    httpserver-go-122-redis-db-2xc9u   standby  <my-org>/httpserver-go-122-redis-db         256MiB  1      go122-redis.internal                     5 minutes ago
```

## Clean up

When done, remove the instances:

```bash title="unikraft"
unikraft instances delete httpserver-go-122-redis-db-2xc9u httpserver-go-122-redis-app-bnnnc
```

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
