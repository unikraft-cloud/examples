# C++ HTTP Server

This guide explains how to create and deploy a simple C++-based HTTP web server.
To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [example repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-gpp13.2/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-gpp13.2/
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
unikraft build . --output <my-org>/httpserver-gpp132:latest
unikraft run --scale-to-zero policy=on,cooldown-time=1000 --metro fra -p 443:8080/tls+http -m 256M --image <my-org>/httpserver-gpp132:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy --scale-to-zero on --scale-to-zero-cooldown 1s -p 443:8080/tls+http -M 256Mi .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         httpserver-gpp132-jzbuo
uuid:         b8e015fd-d006-49d5-849e-3fd497c9159a
state:        starting
image:        <my-org>/httpserver-gpp132
resources:
  memory:     256MiB
  vcpus:      1
service:
  uuid:       fd89859a-cf60-fa1f-1d43-0989a7c18b10
  name:       throbbing-wave-grxjih4t
  domains:
  - fqdn:     throbbing-wave-grxjih4t.fra.unikraft.app
networks:
- uuid:       636ebc7e-bf82-d71d-5432-5445084a4308
  private-ip: 10.0.6.5
  mac:        12:b0:0f:20:02:9d
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: httpserver-gpp132-jzbuo
 ├───────── uuid: b8e015fd-d006-49d5-849e-3fd497c9159a
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://throbbing-wave-grxjih4t.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/httpserver-gpp132@sha256:a58873987104b52c13b79168a2e2f1a81876ba6efacd6dbc98e996afe5c09699
 ├─────── memory: 256 MiB
 ├────── service: throbbing-wave-grxjih4t
 ├─ private fqdn: httpserver-gpp132-jzbuo.internal
 └─── private ip: 10.0.6.5
```

In this case, the instance name is `httpserver-gpp132-jzbuo` and the address is `https://throbbing-wave-grxjih4t.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the C++ HTTP web server:

```bash
curl https://throbbing-wave-grxjih4t.fra.unikraft.app
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
METRO  NAME                     STATE    IMAGE                       ARGS  MEMORY  VCPUS  FQDN                                      CREATED
fra    httpserver-gpp132-jzbuo  running  <my-org>/httpserver-gpp132        256MiB  1      throbbing-wave-grxjih4t.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                     FQDN                                      STATE    STATUS        IMAGE                                                    MEMORY   VCPUS  ARGS  BOOT TIME
httpserver-gpp132-jzbuo  throbbing-wave-grxjih4t.fra.unikraft.app  running  1 minute ago  oci://unikraft.io/<my-org>/httpserver-gpp132@sha256:...  256 MiB  1            15.61 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete httpserver-gpp132-jzbuo
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove httpserver-gpp132-jzbuo
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `http_server.cpp`: the actual C++ HTTP server implementation
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

* `FROM gcc:13.2.0-bookworm AS build`: Build the filesystem from the `bookworm gcc` container image, to [create a base image](https://docs.docker.com/build/building/base-images/).

* `COPY ./http_server.cpp /src/http_server.cpp`: Copy the server implementation file (`http_server.cpp`) in the Docker filesystem (in `/src/http_server.cpp`).

The following options are available for customizing the app:

* If you only update the implementation in the `http_server.cpp` source file, you don't need to make any other changes.

* If you create any new source files, copy them into the app filesystem by using the `COPY` command in the `Dockerfile`.

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
