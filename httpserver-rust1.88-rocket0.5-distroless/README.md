# Distroless Rust (Rocket) HTTP Server

This example uses [`Rocket`](https://rocket.rs/), a popular Rust web framework.
To run it, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-rust1.88-rocket0.5-distroless/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-rust1.88-rocket0.5-distroless
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
unikraft build . --output <my-org>/httpserver-rust188-rocket05-distroless:latest
unikraft run --metro fra \
  -m 256M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/httpserver-rust188-rocket05-distroless:latest
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
name:            httpserver-rust188-rocket05-distroless-cjoq5
uuid:            6e75f64a-3938-44c5-93e4-64688d9dda96
state:           running
image:           <my-org>/httpserver-rust188-rocket05-distroless@sha256:a8c958d85b51fd59c064180b975abe9e74bf5e9639d7a181c59e805e84045386
resources:
  memory:        256MiB
  vcpus:         1
service:
  name:          white-brook-x7190sc4
  uuid:          c206aa80-356b-4f24-afb5-6cc68c796c3f
  domains:
  - fqdn:        white-brook-x7190sc4.fra.unikraft.app
networks:
- uuid:          6abcd057-7ad8-44a5-b6f7-a1e55816a88f
  private-ip:    10.0.9.81
  mac:           12:b0:0a:00:09:51
timestamps:
  created:       just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: httpserver-rust188-rocket05-distroless-cjoq5
 ├───────── uuid: 6e75f64a-3938-44c5-93e4-64688d9dda96
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://white-brook-x7190sc4.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/httpserver-rust188-rocket05-distroless@sha256:23a7a6e155758e6e8f75e9570f0aec5fb744f08c1bad2454d7386367c5ea45d6
 ├─────── memory: 256 MiB
 ├────── service: white-brook-x7190sc4
 ├─ private fqdn: httpserver-rust188-rocket05-distroless-tuwq3.internal
 └─── private ip: 10.0.6.6
```

In this case, the instance name is `httpserver-rust188-rocket05-distroless-tuwq3` and the address is `https://white-brook-x7190sc4.fra.unikraft.app`.
They're different for each run.

Use `curl` to query any of the Rocket server's paths, for example:

```bash
curl https://white-brook-x7190sc4.fra.unikraft.app/wave/Rocketeer/100
```

```text
👋 Hello, 100 year old named Rocketeer!
```

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                                          STATE    IMAGE                                                  ARGS  MEMORY  VCPUS  FQDN                                         CREATED
fra    httpserver-rust188-rocket05-distroless-cjoq5  standby  cosmintanasa47/httpserver-rust188-rocket05-distroless        256MiB  1      white-brook-x7190sc4.fra.unikraft.app        20 minutes ago

```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                                          FQDN                                         STATE    STATUS   IMAGE                                                              MEMORY   VCPUS  ARGS  BOOT TIME
httpserver-rust188-rocket05-distroless-cjoq5  white-brook-x7190sc4.fra.unikraft.app        standby  standby  cosmintanasa47/httpserver-rust188-rocket05-distroless@sha256:a...  256 MiB  1            73.43 ms

```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete httpserver-rust188-rocket05-distroless-cjoq5
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove httpserver-rust188-rocket05-distroless-cjoq5
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
