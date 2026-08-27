# Distroless Rust HTTP Server

This guide explains how to create and deploy a Rust app.
To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-rust1.91` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-rust1.91-distroless/
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
unikraft build . --output <my-org>/httpserver-rust191-distroless:latest
unikraft run --metro fra \
  -m 384M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/httpserver-rust191-distroless:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy \
  -M 384Mi \
  -p 443:8080/tls+http \
  --scale-to-zero on \
  --scale-to-zero-cooldown 1s \
  .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         httpserver-rust191-distroless-pinzf
uuid:         8acb3d35-38ba-4929-81de-950340662c14
state:        starting
image:        <my-org>/httpserver-rust191-distroless
resources:
  memory:     384MiB
  vcpus:      1
service:
  uuid:       3bf42986-3032-1ff2-fe4d-2041db03b628
  name:       snowy-feather-k4pfgl8t
  domains:
  - fqdn:     snowy-feather-k4pfgl8t.fra.unikraft.app
networks:
- uuid:       d64344f4-e159-c7c3-7f1b-ba10bcc60f67
  private-ip: 10.0.2.53
  mac:        12:b0:1d:12:0e:46
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: httpserver-rust191-distroless-pinzf
 ├───────── uuid: 8acb3d35-38ba-4929-81de-950340662c14
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://snowy-feather-k4pfgl8t.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/httpserver-rust191-distroless@sha256:7725556f4db01037438c08d5f934eabe89f33c172b4ae6c7424b3286351619e9
 ├─────── memory: 384 MiB
 ├────── service: snowy-feather-k4pfgl8t
 ├─ private fqdn: httpserver-rust191-distroless-pinzf.internal
 └─── private ip: 10.0.2.53
```

In this case, the instance name is `httpserver-rust191-distroless-pinzf` and the address is `snowy-feather-k4pfgl8t.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance:

```bash
curl https://snowy-feather-k4pfgl8t.fra.unikraft.app
```

```text
Hello, World!
```

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                                 STATE    IMAGE                                  ARGS   MEMORY  VCPUS  FQDN                                     CREATED
fra    httpserver-rust191-dsitroless-pinzf  standby  <my-org>/httpserver-rust191-dsitroless        384MiB  1      snowy-feather-k4pfgl8t.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                                 FQDN                                     STATE    STATUS   IMAGE                                                   MEMORY   VCPUS  ARGS  BOOT TIME 
httpserver-rust191-distroless-pinzf  snowy-feather-k4pfgl8t.fra.unikraft.app  standby  standby  oci://unikraft.io/<my-org>/httpserver-rust191-distroless@sha256:...  384 MiB  1            11.67 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete httpserver-rust191-pinzf
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove httpserver-rust191-pinzf
```

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
