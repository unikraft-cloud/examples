# DuckDB with Go

This guide shows you how to use [DuckDB](https://duckdb.org), an in-process SQL OLAP database management system, in your Go project.

To run this example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/duckdb-go/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/duckdb-go/
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

```ansi
[●] Deployed successfully!
 │
 ├────────── name: duckdb-go-qfd8x
 ├────────── uuid: 90960d27-458b-4dd7-a037-2a9a3a47f095
 ├───────── state: running
 ├─────────── url: https://autumn-gorilla-hg4h6sup.fra.unikraft.app
 ├───────── image: duckdb-go@sha256:6999293f8694ac00beb6a1d639fab8f96f78c2e6ecb8ccb2311539908895a699
 ├───── boot time: 32.12 ms
 ├──────── memory: 128 MiB
 ├─────── service: autumn-gorilla-hg4h6sup
 ├── private fqdn: duckdb-go-qfd8x.internal
 ├──── private ip: 172.16.6.2
 └────────── args: /server
```

In this case, the instance name is `duckdb-go-qfd8x` and the address is `https://autumn-gorilla-hg4h6sup.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of DuckDB.

```bash
curl https://autumn-gorilla-hg4h6sup.fra.unikraft.app
```
```text
id: %d, name: %s 42 John
```

You can list information about the instance by running:

```bash
kraft cloud instance list
```
```ansi
NAME             FQDN                                      STATE    STATUS        IMAGE         MEMORY   VCPUS  ARGS     BOOT TIME
duckdb-go-qfd8x  autumn-gorilla-hg4h6sup.fra.unikraft.app  running  1 minute ago  duckdb-go...  128 MiB  1      /server  32118us
```

When done, you can remove the instance:

```bash
kraft cloud instance remove duckdb-go-qfd8x
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `src/main.go`: the Go web server frontend
* `Kraftfile`: the Unikraft Cloud specification, including command-line arguments
* `Dockerfile`: the Docker-specified app filesystem

The following options are available for customizing the app:

* If you only update the implementation in the `main.go` source file, you don't need to make any other changes.

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
