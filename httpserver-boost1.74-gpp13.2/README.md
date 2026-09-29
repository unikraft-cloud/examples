# C++ Boost HTTP Server

This guide explains how to create and deploy a C++-based HTTP web server using the [Boost](https://www.boost.org/) libraries.
To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [example repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-boost1.74-gpp13.2/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-boost1.74-gpp13.2/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-boost174-gpp132:latest
unikraft run --metro fra \
  -m 256M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/httpserver-boost174-gpp132:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         httpserver-boost174-gpp132-rae7s
uuid:         5a9886fa-f8a3-4860-afcf-d5eb13fdc38d
state:        starting
image:        <my-org>/httpserver-boost174-gpp132
resources:
  memory:     256MiB
  vcpus:      1
service:
  uuid:       52cfb573-c035-9f0c-5db7-63615d26f182
  name:       red-snow-3bn7bzc8
  domains:
  - fqdn:     red-snow-3bn7bzc8.fra.unikraft.app
networks:
- uuid:       44a3d2c5-9ee5-fffc-b72f-d6109072bb8c
  private-ip: 10.0.6.4
  mac:        12:b0:97:bc:2c:03
timestamps:
  created:    just now
```

In this case, the instance name is `httpserver-boost174-gpp132-rae7s` and the address is `https://red-snow-3bn7bzc8.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the C++ Boost HTTP web server:

```bash
curl https://red-snow-3bn7bzc8.fra.unikraft.app
```

```text
Hello, World!
```

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                              STATE    IMAGE                                ARGS  MEMORY  VCPUS  FQDN                                CREATED
fra    httpserver-boost174-gpp132-rae7s  running  <my-org>/httpserver-boost174-gpp132        256MiB  1      red-snow-3bn7bzc8.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete httpserver-boost174-gpp132-rae7s
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `http_server.cpp`: the C++ HTTP server implementation
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

Lines in the `Kraftfile` have the following roles:

* `spec: v0.7`: The current `Kraftfile` specification version is `0.7`.

* `runtime: base`: The Unikraft runtime kernel to use is its base one.

* `rootfs`: Build the app root filesystem.
  `source: ./Dockerfile` means the filesystem is built using the `Dockerfile`.
  `format: erofs` means the filesystem type is [EROFS](https://erofs.docs.kernel.org/).

* `cmd: ["/http_server"]`: Use `/http_server` as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

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

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
