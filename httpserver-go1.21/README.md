# Go HTTP Server

This guide explains how to create and deploy a simple Go-based HTTP web server.
To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-go1.21/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-go1.21/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-go121:latest
unikraft run --metro fra \
  -m 256M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/httpserver-go121:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         httpserver-go121-9a2wv
uuid:         8bb34040-9434-4a28-bd1e-c24ee532e2da
state:        starting
image:        <my-org>/httpserver-go121
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

In this case, the instance name is `httpserver-go121-9a2wv` and the address is `https://red-dew-jtk6yxk1.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Go-based HTTP web server:

```bash
curl https://red-dew-jtk6yxk1.fra.unikraft.app
```

```text
Hello, World!
```

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                    STATE    IMAGE                      ARGS  MEMORY  VCPUS  FQDN                               CREATED
fra    httpserver-go121-9a2wv  running  <my-org>/httpserver-go121        256MiB  1      red-dew-jtk6yxk1.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete httpserver-go121-9a2wv
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `server.go`: the actual Go HTTP server implementation
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

The following options are available for customizing the app:

* If you only update the implementation in the `server.go` source file, you don't need to make any other changes.

* If you create any new source files, copy them into the app filesystem by using the `COPY` command in the `Dockerfile`.

* If you add new source code files, build them using the corresponding `go build` command.

* If you build a new executable, update the `cmd` line in the `Kraftfile` and replace `/server` with the path to the new executable.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
