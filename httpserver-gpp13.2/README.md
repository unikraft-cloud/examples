# C++ HTTP Server

This guide explains how to create and deploy a simple C++-based HTTP web server.
To run this example, follow these steps:

1. Install the CLI and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).

2. Clone the [example repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-gpp13.2/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/httpserver-gpp13.2/
```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

or

```bash title="kraft"
# Set Unikraft Cloud access token
export UKC_TOKEN=token
# Set metro to Frankfurt, DE
export UKC_METRO=fra
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-gpp13.2:latest
unikraft run --metro fra -p 443:8080/tls+http -m 256M --image <my-org>/httpserver-gpp13.2:latest
```

or

```bash title="kraft"
kraft cloud deploy -p 443:8080/tls+http -M 256M .
```

The output shows the instance address and other details:

```text
[●] Deployed successfully!
 │
 ├────────── name: httpserver-gpp13.2-jzbuo
 ├────────── uuid: b8e015fd-d006-49d5-849e-3fd497c9159a
 ├───────── state: running
 ├─────────── url: https://throbbing-wave-grxjih4t.fra.unikraft.app
 ├───────── image: httpserver-gpp13.2@sha256:a58873987104b52c13b79168a2e2f1a81876ba6efacd6dbc98e996afe5c09699
 ├───── boot time: 15.61 ms
 ├──────── memory: 256 MiB
 ├─────── service: throbbing-wave-grxjih4t
 ├── private fqdn: httpserver-gpp13.2-jzbuo.internal
 ├──── private ip: 172.16.6.5
 └────────── args: /http_server
```

In this case, the instance name is `httpserver-gpp13.2-jzbuo` and the address is `https://throbbing-wave-grxjih4t.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the C++ HTTP web server:

```bash
curl https://throbbing-wave-grxjih4t.fra.unikraft.app
```

```text
Hello, World!
```

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

or

```bash title="kraft"
kraft cloud instance list
```

```ansi
NAME                      FQDN                                      STATE    STATUS        IMAGE                                                           MEMORY   VCPUS  ARGS          BOOT TIME
httpserver-gpp13.2-jzbuo  throbbing-wave-grxjih4t.fra.unikraft.app  running  1 minute ago  httpserver-gpp13.2@sha256:a58873987104b52c13b79168a2e2f1a81...  256 MiB  1      /http_server  15614us
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete httpserver-gpp13.2-jzbuo
```

or

```bash title="kraft"
kraft cloud instance remove httpserver-gpp13.2-jzbuo
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `http_server.cpp`: the actual C++ HTTP server implementation
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

Lines in the `Kraftfile` have the following roles:

* `spec: v0.6`: The current `Kraftfile` specification version is `0.6`.

* `runtime: base`: The Unikraft runtime kernel to use is its base one.

* `rootfs`: Build the app root filesystem.
  `source: ./Dockerfile` means the filesystem is built using the `Dockerfile`.
  `type: erofs` means the filesystem type is [EROFS](https://erofs.docs.kernel.org/).

* `cmd: ["/http_server"]`: Use `/http_server` as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

* `FROM --platform=linux/x86_64 gcc:13.2.0-bookworm AS build`: Build the filesystem from the `bookworm gcc` container image, to [create a base image](https://docs.docker.com/build/building/base-images/).

* `COPY ./http_server.cpp /src/http_server.cpp`: Copy the server implementation file (`http_server.cpp`) in the Docker filesystem (in `/src/http_server.cpp`).

The following options are available for customizing the app:

* If you only update the implementation in the `http_server.cpp` source file, you don't need to make any other changes.

* If you create any new source files, copy them into the app filesystem by using the `COPY` command in the `Dockerfile`.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

or

```bash title="kraft"
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft) or the [legacy CLI Reference](https://unikraft.com/docs/cli/kraft/overview).
