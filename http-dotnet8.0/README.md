# .NET

This guide explains how to create and deploy a simple .NET-based HTTP web server.
To run this example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/http-dotnet8.0/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/http-dotnet8.0/
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
kraft cloud deploy -p 443:8080 -M 512 .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: http-dotnet80-dsmkh
 ├────────── uuid: 25459494-cb43-4009-9d05-f0996de5b7e4
 ├───────── state: starting
 ├─────────── url: cold-fog-hl98aw6q.fra.unikraft.app
 ├───────── image: http-dotnet80@sha256:4fad7453995ae96b636696e9929ee0e7376bfbbd63ab9698c1f1e02602aa2575
 ├──────── memory: 512 MiB
 ├─────── service: cold-fog-hl98aw6q
 ├── private fqdn: http-dotnet80-dsmkh.internal
 ├──── private ip: 172.16.3.1
 └────────── args: /usr/bin/app/src
```

In this case, the instance name is `http-dotnet80-dsmkh` and the address is `https://cold-fog-hl98aw6q.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the .NET-based HTTP web server:

```bash
curl https://cold-fog-hl98aw6q.fra.unikraft.app
```

```text
Hello, World!
```

You can list information about the instance by running:

```bash
kraft cloud instance list
```

```ansi
NAME                 FQDN                                STATE    STATUS         IMAGE                                  MEMORY   VCPUS  ARGS              BOOT TIME
http-dotnet80-dsmkh  cold-fog-hl98aw6q.fra.unikraft.app  running  2 minutes ago  http-dotnet80@sha256:4fad7453995ae...  512 MiB  1      /usr/bin/app/src  328.69 ms
```

When done, you can remove the instance:

```bash
kraft cloud instance remove http-dotnet80-dsmkh
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `SimpleHttpServer.cs`: the actual .NET HTTP server
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

Lines in the `Kraftfile` have the following roles:

* `spec: v0.6`: The current `Kraftfile` specification version is `0.6`.

* `runtime: base-compat:latest`: The runtime kernel to use is the base compatibility kernel.

* `rootfs: ./Dockerfile`: Build the app root filesystem using the `Dockerfile`.

* `cmd:`: Use as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

* `WORKDIR /src`: Use the `/src` directory as the working directory.

* `RUN dotnet new console`: Create a new `dotnet` project.

* `RUN rm Program.cs`: Remove template source code file.

* `COPY ./SimpleHttpServer.cs .`: Copy the source code of the HTTP server.

* `RUN dotnet build .`: Build dotnet project.

* `FROM scratch`: Build the filesystem from the [`scratch` container image](https://hub.docker.com/_/scratch/), to [create a base image](https://docs.docker.com/build/building/base-images/).

* `COPY --from=build ...`: Copy on the required files from the filesystem: the binary executable, the .NET framework files and the binary library files.

The following options are available for customizing the app:

* If you only update the implementation in the `SimpleHttpServer.rs` source file, you don't need to make any other changes.

* If you create any new source files, copy them into the app filesystem by using the `COPY` command in the `Dockerfile`.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
