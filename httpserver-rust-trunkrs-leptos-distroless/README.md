# Distroless Rust (Leptos + Trunk) HTTP Server

This guide shows how to deploy a Rust HTTP server using Trunk and Leptos on Unikraft Cloud.
To run it, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-rust-trunkrs-leptos-distroless/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-rust-trunkrs-leptos-distroless/
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
unikraft build . --output <my-org>/httpserver-rust-trunkrs-leptos-distroless:latest
unikraft run --metro fra \
  -m 256M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/httpserver-rust-trunkrs-leptos-distroless:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy --metro fra \
  -M 256Mi \
  -p 443:8080/tls+http \
  --scale-to-zero on \
  --scale-to-zero-cooldown 1s \
  .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         httpserver-rust-trunkrs-leptos-distroless-n2j7k
uuid:         7b8c9d0e-1f2a-3b4c-5d6e-7f8a9b0c1d2e
state:        starting
image:        <my-org>/httpserver-rust-trunkrs-leptos-distroless
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

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: httpserver-rust-trunkrs-leptos-distroless-n2j7k
 ├───────── uuid: 7b8c9d0e-1f2a-3b4c-5d6e-7f8a9b0c1d2e
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://cool-wind-by4hq7nm.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/httpserver-rust-trunkrs-leptos-distroless@sha256:6b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c
 ├─────── memory: 256 MiB
 ├────── service: cool-wind-by4hq7nm
 ├─ private fqdn: httpserver-rust-trunkrs-leptos-distroless-n2j7k.internal
 └─── private ip: 10.0.2.3
```

In this case, the instance name is `httpserver-rust-trunkrs-leptos-distroless-n2j7k` and the address is `https://cool-wind-by4hq7nm.fra.unikraft.app`.
They're different for each run.

The command will deploy files in the current directory.

After deploying, you can query the service using the provided URL.

To run locally:

```bash
trunk serve
```

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                                             STATE    IMAGE                                               ARGS  MEMORY  VCPUS  FQDN                                 CREATED
fra    httpserver-rust-trunkrs-leptos-distroless-n2j7k  running  <my-org>/httpserver-rust-trunkrs-leptos-distroless        256MiB  1      cool-wind-by4hq7nm.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                                             FQDN                                 STATE    STATUS        IMAGE                                                                 MEMORY   VCPUS  ARGS  BOOT TIME
httpserver-rust-trunkrs-leptos-distroless-n2j7k  cool-wind-by4hq7nm.fra.unikraft.app  running  1 minute ago  oci://unikraft.io/<my-org>/httpserver-rust-trunkrs-leptos-distroless@sha256:...  256 MiB  1            8.42 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete <instance-name>
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove <instance-name>
```


## Learn more

- [leptos](https://leptos.dev)
- [trunkrs](https://trunkrs.dev)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)


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
