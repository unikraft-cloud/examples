# Redis

This guides shows you  how to use [Redis](https://redis.io), an open source in-memory storage, used as a distributed, in-memory key–value database, cache and message broker, with optional durability.

To run it example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/redis/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/redis/
```

Make sure to log into Unikraft Cloud by setting your token and a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash
export UKC_TOKEN=token
# Set metro to Frankfurt, DE
export UKC_METRO=fra
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash
kraft cloud deploy -p 6379:6379/tls -M 512 .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: redis-alb4r
 ├────────── uuid: d3c3141b-97b2-4e1d-87ae-39e4f14ab49e
 ├───────── state: running
 ├────────── fqdn: rough-wind-8vxrd1ms.fra.unikraft.app
 ├───────── image: redis@sha256:9665c51faf7deb538cf7907b012b55700cad08cd391f5ba099d95d018c8da7d
 ├───── boot time: 26.13 ms
 ├──────── memory: 512 MiB
 ├─────── service: rough-wind-8vxrd1ms
 ├── private fqdn: redis-alb4r.internal
 ├──── private ip: 172.16.6.2
 └────────── args: /usr/bin/redis-server /etc/redis/redis.conf
```

In this case, the instance name is `redis-alb4r` which is different for every run.

To test the deployment, first forward the port with the `kraft cloud tunnel` command:

```bash
kraft cloud tunnel 6379:memcached-arkv7:6379
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

To disconnect, kill the `tunnel` command with ctrl-C.

> **Note:**
> This guide uses `kraft cloud tunnel` only when a service doesn't support TLS and isn't HTTP-based (TLS/SNI determines the correct instance to send traffic to).
> Also note that the `tunnel` command isn't needed when connecting via an instance's private IP/FQDN.
> For example, when a Redis instance serves as a cache server to
> another instance that acts as a frontend and which **does** support TLS.

You can list information about the instance by running:

```bash
kraft cloud instance list
```
```ansi
NAME         FQDN                                  STATE    STATUS        IMAGE                   MEMORY   VCPUS  ARGS                               BOOT TIME
redis-alb4r  rough-wind-8vxrd1ms.fra.unikraft.app  running  1 minute ago  redis@sha256:9665c5...  512 MiB  1      /usr/bin/redis-server /etc/red...  26131us
```

When done, you can remove the instance:

```bash
kraft cloud instance remove redis-alb4r
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification, including command-line arguments
* `Dockerfile`: In case you need to add files to your instance's rootfs

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
