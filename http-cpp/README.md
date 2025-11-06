# C++

This guide explains how to create and deploy a simple C++-based HTTP web server.
To run this example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [example repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/http-cpp/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/http-cpp/
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
kraft cloud deploy -p 443:8080 .
```

The output shows the instance address and other details:

```text
[●] Deployed successfully!
 │
 ├────────── name: http-cpp-jzbuo
 ├────────── uuid: b8e015fd-d006-49d5-849e-3fd497c9159a
 ├───────── state: running
 ├─────────── url: https://throbbing-wave-grxjih4t.fra.unikraft.app
 ├───────── image: http-cpp@sha256:a58873987104b52c13b79168a2e2f1a81876ba6efacd6dbc98e996afe5c09699
 ├───── boot time: 15.61 ms
 ├──────── memory: 128 MiB
 ├─────── service: throbbing-wave-grxjih4t
 ├── private fqdn: http-cpp-jzbuo.internal
 ├──── private ip: 172.16.6.5
 └────────── args: /http_server
```

In this case, the instance name is `http-cpp-jzbuo` and the address is `https://throbbing-wave-grxjih4t.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the C++ HTTP web server:

```bash
curl https://throbbing-wave-grxjih4t.fra.unikraft.app
```
```text
Hello, World!
```

You can list information about the instance by running:

```bash
kraft cloud instance list
```
```ansi
NAME            FQDN                                      STATE    STATUS        IMAGE                                                           MEMORY   VCPUS  ARGS          BOOT TIME
http-cpp-jzbuo  throbbing-wave-grxjih4t.fra.unikraft.app  running  1 minute ago  http-cpp@sha256:a58873987104b52c13b79168a2e2f1a81876ba6efac...  128 MiB  1      /http_server  15614us
```

When done, you can remove the instance:

```bash
kraft cloud instance remove http-cpp-jzbuo
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `http_server.cpp`: the actual C++ HTTP server
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

Lines in the `Kraftfile` have the following roles:

* `spec: v0.6`: The current `Kraftfile` specification version is `0.6`.

* `runtime: base`: The Unikraft runtime kernel to use is its base one.

* `rootfs: ./Dockerfile`: Build the app root filesystem using the `Dockerfile`.

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

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
