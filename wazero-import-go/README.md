# Wazero

This example comes from [Wazero's "import go" example](https://github.com/tetratelabs/wazero/tree/main/examples/import-go)
and shows how to define, import and call a wasm blob from Go and run it on Unikraft Cloud.

To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/wazero-import-go/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/wazero-import-go/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/wazero-import-go:latest
unikraft run --metro fra \
  -m 512M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/wazero-import-go:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         wazero-import-go-r4dx8
uuid:         a763e1c3-bb38-475f-95b6-1e78d8ca74fc
state:        starting
image:        <my-org>/wazero-import-go
resources:
  memory:     512MiB
  vcpus:      1
service:
  uuid:       f38a171d-e283-24ca-1158-c7907948071e
  name:       cool-morning-camrrhsa
  domains:
  - fqdn:     cool-morning-camrrhsa.fra.unikraft.app
networks:
- uuid:       bc4bb64c-8185-3b83-8693-b1464ab4723e
  private-ip: 10.0.6.7
  mac:        12:b0:05:55:02:fe
timestamps:
  created:    just now
```

In this case, the instance name is `wazero-import-go-r4dx8` and the address is `https://cool-morning-camrrhsa.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Go/wazero server:

```bash
curl https://cool-morning-camrrhsa.fra.unikraft.app
```

```text
println >> 24
log_i32 >> 24
```

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                    STATE    IMAGE                      ARGS  MEMORY  VCPUS  FQDN                                    CREATED
fra    wazero-import-go-r4dx8  running  <my-org>/wazero-import-go        512MiB  1      cool-morning-camrrhsa.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete wazero-import-go-r4dx8
```

## Background

WebAssembly has neither a mechanism to get the current year, nor one to print to the console, so this example defines these in Go.
Like Go, WebAssembly functions are namespaced into modules instead of packages.
With Go only exported functions can import into another module.
`age-calculator.go` shows how to export functions using [HostModuleBuilder](https://pkg.go.dev/github.com/tetratelabs/wazero#HostModuleBuilder) and how a WebAssembly module defined in its [text format](https://www.w3.org/TR/2019/REC-wasm-core-1-20191205/#text-format%E2%91%A0) imports it.
This only uses the text format for demonstration purposes, to show you what's going on.
It's likely, you will use another language to compile a Wasm (WebAssembly Module) binary, such as TinyGo.
Regardless of how wasm produces, the export/import mechanics are the same!

### Using WASI

WebAssembly System Interface (WASI) is a modular system interface for WebAssembly.
This uses an ad-hoc Go-defined function to print to the console.
An emerging specification standardizes system calls (like Go's [x/sys](https://pkg.go.dev/golang.org/x/sys/unix)) called WebAssembly System Interface [(WASI)](https://github.com/WebAssembly/WASI).
While this isn't yet a W3C standard, wazero includes a [wasi package](https://pkg.go.dev/github.com/tetratelabs/wazero/wasi).

## Customize your app

To customize the app, update the files in the repository, listed below:

* `agecalculator.go`: The Go web server that calls the WASM/Wazero blog for the age calculation
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
