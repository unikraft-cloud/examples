# Redis

This guide shows you how to use [Redis](https://redis.io), an open source in-memory storage, used as a distributed, in-memory key–value database, cache and message broker, with optional durability.

To run it, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/redis7.2/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/redis7.2/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/redis72:latest
unikraft run --metro fra \
  -m 512M \
  -p 6379:6379/tls \
  --scale-to-zero policy=off \
  --image <my-org>/redis72:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         redis72-alb4r
uuid:         d3c3141b-97b2-4e1d-87ae-39e4f14ab49e
state:        starting
image:        <my-org>/redis72
resources:
  memory:     512MiB
  vcpus:      1
service:
  uuid:       7a4f2b3c-1d8e-4a92-b3f5-e6c1d2a3b4e5
  name:       rough-wind-8vxrd1ms
  domains:
  - fqdn:     rough-wind-8vxrd1ms.fra.unikraft.app
networks:
- uuid:       9b5e1f8d-3c2a-7b46-d1e9-f2a3b4c5d6e7
  private-ip: 10.0.3.2
  mac:        12:b0:4e:20:b3:e7
timestamps:
  created:    just now
```

In this case, the instance name is `redis72-alb4r` which is different for every run.

To test the deployment, first forward the port using `socat`:

```bash
socat TCP-LISTEN:6379,fork OPENSSL:rough-wind-8vxrd1ms.fra.unikraft.app:6379,verify=0
```

Then, from another console, you can now use the `redis-benchmark` client to connect to Redis, for example:

```console
redis-benchmark -t ping,set,get -n 10000
```

You should see output like:

```ansi
====== PING_INLINE ======
  10000 requests completed in 32.03 seconds
  50 parallel clients
  3 bytes payload
  keep alive: 1
  host configuration "save":
  host configuration "appendonly": no
  multi-thread: no

0.01% <= 138 milliseconds
0.05% <= 139 milliseconds
2.34% <= 140 milliseconds
4.49% <= 141 milliseconds
8.57% <= 142 milliseconds
16.06% <= 143 milliseconds
21.83% <= 144 milliseconds
26.25% <= 145 milliseconds
34.54% <= 146 milliseconds
...
```

To disconnect, kill the `socat` command with ctrl-C.

> **Note:**
> This guide uses `socat` for port forwarding only when a service doesn't support TLS and isn't HTTP-based (TLS/SNI determines the correct instance to send traffic to).
> Also note that port forwarding isn't needed when connecting via an instance's private IP/FQDN.
> For example, when a Redis instance serves as a cache server to
> another instance that acts as a frontend and which **does** support TLS.

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME           STATE    IMAGE              ARGS  MEMORY  VCPUS  FQDN                                  CREATED
fra    redis72-alb4r  running  <my-org>/redis72        512MiB  1      rough-wind-8vxrd1ms.fra.unikraft.app  1 minute ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete redis72-alb4r
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification, including command-line arguments
* `Dockerfile`: In case you need to add files to your instance's rootfs

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
