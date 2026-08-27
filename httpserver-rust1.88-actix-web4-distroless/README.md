# Distroless Rust (Actix Web) HTTP Server

This example uses [`actix-web`](https://actix.rs), a popular Rust web framework.
To run it, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

1. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-rust1.88-actix-web4-distroless/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-rust1.88-actix-web4-distroless/
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
unikraft build . --output <my-org>/httpserver-rust188-actix-web4-dsitroless:latest
unikraft run --metro fra \
  -m 256M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/httpserver-rust188-actix-web4-distroless:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy \
  -M 256Mi \
  -p 443:8080/tls+http \
  --scale-to-zero on \
  --scale-to-zero-cooldown 1s \
  .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:           fra
name:            httpserver-rust188-actix-web4-distroless-x5cck
uuid:            aa7e8132-e993-4c4d-b1bf-a68475d9ec19
state:           running
image:           <my-org>/httpserver-rust188-actix-web4-distroless@sha256:3cb8322258840ec48037c4724465e98a4dc57e022e8042dd4b9324a03ffaf702
resources:
  memory:        256MiB
  vcpus:         1
service:
  name:          floral-water-sndspsy3
  uuid:          be12ef58-4726-41a0-a9f6-0c55fa084528
  domains:
  - fqdn:        floral-water-sndspsy3.fra.unikraft.app
networks:
- uuid:          9228dcac-2475-45cc-89bc-e5e097e5724f
  private-ip:    10.0.18.201
  mac:           12:b0:0a:00:12:c9
timestamps:
  created:       just now

```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: httpserver-rust188-actix-web4-distroless-x5cck
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://floral-water-sndspsy3.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/httpserver-rust188-actix-web4-distroless@sha256:3cb8322258840ec48037c4724465e98a4dc57e022e8042dd4b9324a03ffaf702
 ├─────── memory: 256 MiB
 ├────── service: loral-water-sndspsy3
 ├─ private fqdn: httpserver-rust188-actix-web4-distroless-x5cck.internal
 └─── private ip: 10.0.3.3
```

In this case, the instance name is `httpserver-rust188-actix-web4-distroless-x5cck` and the address is `https://floral-water-sndspsy3.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Rust-based HTTP web server:

```bash
curl https://floral-water-sndspsy3.fra.unikraft.app
curl https://floral-water-sndspsy3.fra.unikraft.app/hey
```

```text
Hello, World!
Hey there!
```

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                                            STATE    IMAGE                                                    ARGS  MEMORY  VCPUS  FQDN                                      CREATED
fra    httpserver-rust188-actix-web4-distroless-x5cck  standby  cosmintanasa47/httpserver-rust188-actix-web4-distroless        256MiB  1      floral-water-sndspsy3.fra.unikraft.app    11 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                                            FQDN                                      STATE    STATUS   IMAGE                                                             MEMORY   VCPUS  ARGS  BOOT TIME
httpserver-rust188-actix-web4-distroless-x5cck  floral-water-sndspsy3.fra.unikraft.app    standby  standby  cosmintanasa47/httpserver-rust188-actix-web4-distroless@sha25...  256 MiB  1            74.36 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete httpserver-rust188-actix-web4-distroless-x5cck
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove httpserver-rust188-actix-web4-distroless-x5cck
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `src/main.rs`: the actual server implementation
* `Cargo.toml`: the Cargo package manager configuration file
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

The following options are available for customizing the app:

* If you only update the implementation in the `src/main.rs` source file, you don't need to make any other changes.

* If you create any new source files, copy them into the app filesystem by using the `COPY` command in the `Dockerfile`.
  If you add new Rust source code files, be sure to configure required dependencies in the `Cargo.toml` file.

* If you build a new executable, update the `cmd` line in the `Kraftfile` and replace `/server` with the path to the new executable.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

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
