# Wazero

This example comes from [Wazero's "import go" example](https://github.com/tetratelabs/wazero/tree/main/examples/import-go)
and shows how to define, import and call a wasm blob from Go and run it on Unikraft Cloud.
To run this it, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/wazero-import-go/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/wazero-import-go/
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
kraft cloud deploy -p 443:8080 . /age-calculator 2000
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: wazero-import-go-r4dx8
 ├────────── uuid: a763e1c3-bb38-475f-95b6-1e78d8ca74fc
 ├───────── state: running
 ├─────────── url: https://cool-morning-camrrhsa.fra.unikraft.app
 ├───────── image: wazero-import-go@sha256:865700d358ffb2751888798ec8f302d23310b1fcf84f4d3f17f79fc25ff71153
 ├───── boot time: 20.04 m
 ├──────── memory: 512 MiB
 ├─────── service: cool-morning-camrrhsa
 ├── private fqdn: wazero-import-go-r4dx8.internal
 ├──── private ip: 172.16.6.7
 └────────── args: /age-calculator 2000
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

```bash
kraft cloud instance list
```
```ansi
NAME                    FQDN                                    STATE    STATUS        IMAGE                  MEMORY   VCPUS  ARGS                  BOOT TIME
wazero-import-go-r4dx8  cool-morning-camrrhsa.fra.unikraft.app  running  1 minutes ag  wazero-import-go@s...  512 MiB  1      /age-calculator 2000  20040us
```

When done, you can remove the instance:

```bash
kraft cloud instance remove wazero-import-go-r4dx8
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

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
