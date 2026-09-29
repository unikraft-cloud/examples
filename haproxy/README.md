# HAProxy

This guide shows you how to use [HAProxy](https://www.haproxy.org).
HAProxy is a free and open source software that provides a high availability load balancer and reverse proxy for TCP and HTTP-based apps that spreads requests across many servers.

To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/haproxy/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/haproxy/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/haproxy:latest
unikraft run --metro fra \
  -m 256M \
  -p 443:8404/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/haproxy:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         haproxy-rfx6z
uuid:         09bd081e-e082-4f73-8ba8-531123a39e2e
state:        starting
image:        <my-org>/haproxy
resources:
  memory:     256MiB
  vcpus:      1
service:
  uuid:       c349833c-dacc-7763-306e-553f512c4d0e
  name:       cool-paper-svzzr3qq
  domains:
  - fqdn:     cool-paper-svzzr3qq.fra.unikraft.app
networks:
- uuid:       494814aa-38cc-c4ed-dcad-5b7173b3033b
  private-ip: 10.0.6.5
  mac:        12:b0:a4:a5:0d:24
timestamps:
  created:    just now
```

In this case, the instance name is `haproxy-rfx6z` and the address is `https://cool-paper-svzzr3qq.fra.unikraft.app`.
They're different for each run.

To test, point your browser at the `/stats` endpoint (for example, `https://cool-paper-svzzr3qq.fra.unikraft.app/stats`).

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME           STATE    IMAGE             ARGS  MEMORY  VCPUS  FQDN                                  CREATED
fra    haproxy-rfx6z  running  <my-org>/haproxy        256MiB  1      cool-paper-svzzr3qq.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete haproxy-rfx6z
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
