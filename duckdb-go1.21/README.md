# DuckDB with Go

This guide shows you how to use [DuckDB](https://duckdb.org), an in-process SQL OLAP database management system, in your Go project.

To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/duckdb-go1.21/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/duckdb-go1.21/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/duckdb-go121:latest
unikraft run --metro fra \
  -m 256M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000,stateful=true \
  --image <my-org>/duckdb-go121:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         duckdb-go121-qfd8x
uuid:         90960d27-458b-4dd7-a037-2a9a3a47f095
state:        starting
image:        <my-org>/duckdb-go121
resources:
  memory:     256MiB
  vcpus:      1
service:
  uuid:       0e3c61f1-5ad3-7d75-ceaf-079ea83394f6
  name:       autumn-gorilla-hg4h6sup
  domains:
  - fqdn:     autumn-gorilla-hg4h6sup.fra.unikraft.app
networks:
- uuid:       0f66c51a-dcad-94fc-d0a8-b0570e3d1b97
  private-ip: 10.0.6.2
  mac:        12:b0:31:d1:4b:90
timestamps:
  created:    just now
```

In this case, the instance name is `duckdb-go121-qfd8x` and the address is `https://autumn-gorilla-hg4h6sup.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of DuckDB.

```bash
curl https://autumn-gorilla-hg4h6sup.fra.unikraft.app
```

```text
id: %d, name: %s 42 John
```

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                STATE    IMAGE                  ARGS  MEMORY  VCPUS  FQDN                                      CREATED
fra    duckdb-go121-qfd8x  running  <my-org>/duckdb-go121        256MiB  1      autumn-gorilla-hg4h6sup.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete duckdb-go121-qfd8x
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

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
