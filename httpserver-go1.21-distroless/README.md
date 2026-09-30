# Go HTTP Server (Distroless)

This guide explains how to create and deploy a simple Go-based HTTP web server, using a [distroless](https://github.com/GoogleContainerTools/distroless) base image (`gcr.io/distroless/static-debian13`) for the runtime stage instead of a bare `scratch` image.

This example is a variant of [`httpserver-go1.21`](../httpserver-go1.21).

## Note on this variant

The Go binary in this example is already built as a fully static executable (`CGO_ENABLED`-free, `-static-pie`, `netgo`), so it runs correctly on a bare `scratch` image without any manual library copying — unlike the Java and Python examples in this repository. The switch to `gcr.io/distroless/static-debian13` here is mainly about consistency with the rest of the distroless examples, and it adds a small set of useful defaults out of the box (CA certificates, `/etc/passwd`, timezone data), which are helpful if the server is later extended to make outbound HTTPS requests.

To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-go1.21-distroless/` directory:

```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-go1.21-distroless/
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
unikraft build . --output <my-org>/httpserver-go121-distroless:latest
unikraft run --metro fra \
  -m 256M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/httpserver-go121-distroless:latest
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
metro:        fra
name:         httpserver-go121-distroless-9a2wv
uuid:         8bb34040-9434-4a28-bd1e-c24ee532e2da
state:        starting
image:        <my-org>/httpserver-go121-distroless
resources:
  memory:     256MiB
  vcpus:      1
service:
  uuid:       cc4ed399-32da-eb56-3671-b477108d1040
  name:       red-dew-jtk6yxk1
  domains:
  - fqdn:     red-dew-jtk6yxk1.fra.unikraft.app
networks:
- uuid:       51f79dc1-e989-908d-894b-bdf0a87e7901
  private-ip: 10.0.3.3
  mac:        12:b0:57:91:bb:a5
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: httpserver-go121-distroless-9a2wv
 ├───────── uuid: 8bb34040-9434-4a28-bd1e-c24ee532e2da
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://red-dew-jtk6yxk1.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/httpserver-go121-distroless@sha256:b16d61bb7898e764d8c11ab5a0b995e8c25a25b5ff89e161fc994ebf25a75680
 ├─────── memory: 256 MiB
 ├────── service: red-dew-jtk6yxk1
 ├─ private fqdn: httpserver-go121-distroless-9a2wv.internal
 └─── private ip: 10.0.3.3
```

In this case, the instance name is `httpserver-go121-distroless-9a2wv` and the address is `https://red-dew-jtk6yxk1.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Go-based HTTP web server:

```bash
curl https://red-dew-jtk6yxk1.fra.unikraft.app
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
METRO  NAME                                STATE    IMAGE                                  ARGS  MEMORY  VCPUS  FQDN                               CREATED
fra    httpserver-go121-distroless-9a2wv  running  <my-org>/httpserver-go121-distroless        256MiB  1      red-dew-jtk6yxk1.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                                FQDN                               STATE    STATUS        IMAGE                                                               MEMORY   VCPUS  ARGS  BOOT TIME
httpserver-go121-distroless-9a2wv  red-dew-jtk6yxk1.fra.unikraft.app  running  1 minute ago  oci://unikraft.io/<my-org>/httpserver-go121-distroless@sha256:...  256 MiB  1            9.32 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete httpserver-go121-distroless-9a2wv
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove httpserver-go121-distroless-9a2wv
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `server.go`: the actual Go HTTP server implementation
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

Lines in the `Dockerfile` have the following roles:

* `FROM --platform=linux/x86_64 golang:1.21.3-bookworm AS build`: Build the app using the Go 1.21.3 toolchain.

* `RUN go build -buildmode=pie -ldflags "-linkmode external -extldflags -static-pie" -tags netgo -o /server server.go`: Compile a fully static, position-independent executable, avoiding any dynamic C library dependencies.

* `FROM --platform=linux/x86_64 gcr.io/distroless/static-debian13`: Build the runtime filesystem from Google's [distroless](https://github.com/GoogleContainerTools/distroless) minimal static base image, instead of a bare `scratch` image.

* `COPY --from=build /server /server`: Copy the compiled binary into the app filesystem.

The following options are available for customizing the app:

* If you only update the implementation in the `server.go` source file, you don't need to make any other changes.

* If you create any new source files, copy them into the app filesystem by using the `COPY` command in the `Dockerfile`.

* If you add new source code files, build them using the corresponding `go build` command.

* If you build a new executable, update the `cmd` line in the `Kraftfile` and replace `/server` with the path to the new executable.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

## Learn more

- [Go Documentation](https://go.dev/doc/)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Distroless Images](https://github.com/GoogleContainerTools/distroless)

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
