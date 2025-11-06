# Golang

This guide explains how to create and deploy a simple Go-based HTTP web server.
To run this example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/http-go1.21/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/http-go1.21/
```

Make sure to log into Unikraft Cloud by setting your token and a [metro](/docs/metros#available) close to you.
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

```ansi
[●] Deployed successfully!
 │
 ├────────── name: http-go121-9a2wv
 ├────────── uuid: 8bb34040-9434-4a28-bd1e-c24ee532e2da
 ├───────── state: running
 ├─────────── url: https://red-dew-jtk6yxk1.fra.unikraft.app
 ├───────── image: http-go121@sha256:b16d61bb7898e764d8c11ab5a0b995e8c25a25b5ff89e161fc994ebf25a75680
 ├───── boot time: 11.05 ms
 ├──────── memory: 128 MiB
 ├─────── service: red-dew-jtk6yxk1
 ├── private fqdn: http-go121-9a2wv.internal
 ├──── private ip: 172.16.3.3
 └────────── args: /server
```

In this case, the instance name is `http-go121-9a2wv` and the address is `https://red-dew-jtk6yxk1.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Lua-based HTTP web server:

```bash
curl https://red-dew-jtk6yxk1.fra.unikraft.app
```
```text
hello, world!
```

You can list information about the instance by running:

```bash
kraft cloud instance list
```
```ansi
NAME              FQDN                               STATE    STATUS        IMAGE                                        MEMORY   VCPUS  ARGS     BOOT TIME
http-go121-9a2wv  red-dew-jtk6yxk1.fra.unikraft.app  running  1 minute ago  alex/http-go121@sha256:b16d61bb7898e764d...  128 MiB  1      /server  9324us
```

When done, you can remove the instance:

```bash
kraft cloud instance delete http-go121-9a2wv
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `server.go`: the actual Go HTTP server
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

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
