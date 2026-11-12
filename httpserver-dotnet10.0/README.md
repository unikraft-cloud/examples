# .NET HTTP Server

This guide explains how to create and deploy a simple .NET-based HTTP web server.
To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-dotnet10.0/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-dotnet10.0/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-dotnet100:latest
unikraft run --metro fra \
  -m 512M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000,stateful=true \
  --image <my-org>/httpserver-dotnet100:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         httpserver-dotnet100-dsmkh
uuid:         25459494-cb43-4009-9d05-f0996de5b7e4
state:        starting
image:        <my-org>/httpserver-dotnet100
resources:
  memory:     512MiB
  vcpus:      1
service:
  uuid:       35a84131-01b7-b3cd-03a4-7acdd2c4f5f9
  name:       cold-fog-hl98aw6q
  domains:
  - fqdn:     cold-fog-hl98aw6q.fra.unikraft.app
networks:
- uuid:       d4ddf6b4-91e5-8692-03a2-1e42552f6dbe
  private-ip: 10.0.3.1
  mac:        12:b0:c0:f1:05:bd
timestamps:
  created:    just now
```

In this case, the instance name is `httpserver-dotnet100-dsmkh` and the address is `https://cold-fog-hl98aw6q.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the .NET-based HTTP web server:

```bash
curl https://cold-fog-hl98aw6q.fra.unikraft.app
```

```text
Hello, World!
```

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                        STATE    IMAGE                          ARGS  MEMORY  VCPUS  FQDN                                CREATED
fra    httpserver-dotnet100-dsmkh  running  <my-org>/httpserver-dotnet100        512MiB  1      cold-fog-hl98aw6q.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete httpserver-dotnet100-dsmkh
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `SimpleHttpServer.cs`: the actual .NET HTTP server implementation
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

Lines in the `Kraftfile` have the following roles:

* `spec: v0.7`: The current `Kraftfile` specification version is `0.7`.

* `rootfs`: Build the app root filesystem.
  `source: ./Dockerfile` means the filesystem is built using the `Dockerfile`.
  `format: erofs` means the filesystem type is [EROFS](https://erofs.docs.kernel.org/).

* `cmd:`: Use as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

* `FROM --platform=$BUILDPLATFORM mcr.microsoft.com/dotnet/sdk:10.0-noble AS build`: Build the app with the .NET SDK on the build machine.

* `WORKDIR /src`: Use the `/src` directory as the working directory.

* `RUN dotnet new console`: Create a new `dotnet` project.

* `RUN rm Program.cs`: Remove template source code file.

* `COPY ./SimpleHttpServer.cs .`: Copy the source code of the HTTP server.

* `RUN dotnet publish -a "$TARGETARCH" --self-contained -o /app`: Build a self-contained app for the target architecture.

* `FROM mcr.microsoft.com/dotnet/runtime-deps:10.0-noble AS runtime`: Use the .NET runtime dependencies image for the target architecture.

* `RUN ... lddtree ...`: Collect the app, the system libraries that it uses, and the ICU libraries in `/rootfs`.
  .NET loads the ICU libraries at runtime for globalization support.

* `FROM scratch`: Build the filesystem from the [`scratch` container image](https://hub.docker.com/_/scratch/), to [create a base image](https://docs.docker.com/build/building/base-images/).

* `COPY --from=runtime /rootfs /`: Copy the collected files to the app filesystem.

The following options are available for customizing the app:

* If you only update the implementation in the `SimpleHttpServer.cs` source file, you don't need to make any other changes.

* If you create any new source files, copy them to `/src` in the build stage with a `COPY` command in the `Dockerfile`.
  `dotnet publish` includes them in `/app`, and the `runtime` stage copies `/app` to `/rootfs`.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
