# Flask + Redis HTTP Server

This guide explains how to create and deploy a [Flask](https://flask.palletsprojects.com/en/3.0.x/) app with a [Redis](https://redis.io/) database on Unikraft Cloud.
The example consists of two services: a Flask web server that increments a page view counter stored in Redis.

To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-flask-redis` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-flask-redis/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

### Deploy Redis

First, deploy the Redis instance.
Redis is an internal service (not publicly accessible), reached via the `redis.internal` domain:

```bash title="unikraft"
unikraft build redis/ --output <my-org>/redis:latest
unikraft run --metro fra \
  -m 256M \
  --scale-to-zero policy=idle,cooldown-time=1000,stateful=true \
  --domain redis.internal \
  --image <my-org>/redis:latest
```

The output shows the Redis instance details:

```ansi title="unikraft"
metro:         fra
name:          redis-09p2q
uuid:          0355f93a-7b60-4ade-9359-b01671e812b3
state:         starting
image:         <my-org>/redis
resources:
  memory:      256MiB
  vcpus:       1
service:
  uuid:        19c050b2-b5c9-4e8e-9d25-a9053ff09270
  name:        damp-brook-xmmmwzwo
  domains:
  - fqdn:      redis.internal
networks:
- uuid:        97df34f7-63bc-4f02-a1b4-5ba07278de00
  private-ip:  10.0.0.41
  mac:         12:b0:0a:00:00:29
timestamps:
  created:     just now
scale-to-zero: policy=idle,stateful=true,cooldown-time=1s
```

### Deploy Flask

Next, deploy the Flask web server.
It connects to Redis using the `REDIS_HOST` and `REDIS_PORT` environment variables:

```bash title="unikraft"
unikraft build flask/ --output <my-org>/flask:latest
unikraft run --metro fra \
  -m 512M \
  -p 443:8000/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --env REDIS_HOST=redis.internal \
  --env REDIS_PORT=6379 \
  --image <my-org>/flask:latest
```

The output shows the Flask instance details:

```ansi title="unikraft"
metro:          fra
name:           flask-q62qa
uuid:           d081ec92-629b-45b3-8caf-059e0a87dffd
state:          starting
image:          <my-org>/flask
runtime:
  env:
    REDIS_HOST: redis.internal
    REDIS_PORT: 6379
resources:
  memory:       512MiB
  vcpus:        1
service:
  uuid:         ac1cd90e-a1fe-478c-8f58-8598fa80c494
  name:         hidden-silence-htyml3s2
  domains:
  - fqdn:       hidden-silence-htyml3s2.fra.unikraft.app
networks:
- uuid:         d2f3d024-3082-4e98-be22-f36df84263a1
  private-ip:   10.0.0.53
  mac:          12:b0:0a:00:00:35
timestamps:
  created:      just now
scale-to-zero:  policy=on,cooldown-time=1s
```

In this case, the Flask instance address is `https://withered-cherry-xfcrfp93.fra.unikraft.app`.
It's different for each run.

### Test the deployment

Use `curl` to query the Flask instance.
Each request increments the Redis counter:

```bash
curl https://withered-cherry-xfcrfp93.fra.unikraft.app
```

```text
This webpage has been viewed 1 time(s)
```

```bash
curl https://withered-cherry-xfcrfp93.fra.unikraft.app
```

```text
This webpage has been viewed 2 time(s)
```

You can list information about the instances by running:

```bash title="unikraft"
unikraft instances list
```

### Clean up

When done, remove the instances:

```bash title="unikraft"
unikraft instances delete flask-q62qa
unikraft instances delete redis-09p2q
```

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
