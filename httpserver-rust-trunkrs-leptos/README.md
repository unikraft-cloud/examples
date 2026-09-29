# Rust (Leptos + Trunk) HTTP Server

This guide shows how to deploy a Rust HTTP server using Trunk and Leptos on Unikraft Cloud.
To run it, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-rust-trunkrs-leptos/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-rust-trunkrs-leptos/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-rust-trunkrs-leptos:latest
unikraft run --metro fra \
  -m 256M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/httpserver-rust-trunkrs-leptos:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         httpserver-rust-trunkrs-leptos-n2j7k
uuid:         7b8c9d0e-1f2a-3b4c-5d6e-7f8a9b0c1d2e
state:        starting
image:        <my-org>/httpserver-rust-trunkrs-leptos
resources:
  memory:     256MiB
  vcpus:      1
service:
  uuid:       8c9d0e1f-2a3b-4c5d-6e7f-8a9b0c1d2e3f
  name:       cool-wind-by4hq7nm
  domains:
  - fqdn:     cool-wind-by4hq7nm.fra.unikraft.app
networks:
- uuid:       9d0e1f2a-3b4c-5d6e-7f8a-9b0c1d2e3f4a
  private-ip: 10.0.2.3
  mac:        12:b0:7d:4f:bc:a6
timestamps:
  created:    just now
```

In this case, the instance name is `httpserver-rust-trunkrs-leptos-n2j7k` and the address is `https://cool-wind-by4hq7nm.fra.unikraft.app`.
They're different for each run.

The command will deploy files in the current directory.

After deploying, you can query the service using the provided URL.

To run locally:

```bash
trunk serve
```

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                                  STATE    IMAGE                                    ARGS  MEMORY  VCPUS  FQDN                                 CREATED
fra    httpserver-rust-trunkrs-leptos-n2j7k  running  <my-org>/httpserver-rust-trunkrs-leptos        256MiB  1      cool-wind-by4hq7nm.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete <instance-name>
```

## Learn more

- [leptos](https://leptos.dev)
- [trunkrs](https://trunkrs.dev)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)


Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
