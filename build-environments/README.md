# Build and Test Environments with ROMs

Build and test workloads need to run frequently changing code in a stable, isolated runtime, without rebuilding a full image for every change.

This guide shows how to deploy a Go runtime that compiles ROM-provided code before execution.
The base image contains a generic server and Go toolchain.
Each ROM only contains a `rom.go` file, which the instance compiles into a Go plugin (`.so`) at startup.
Because only the ROM changes between runs, you update the code under test by pushing a small ROM while the runtime stays as it is.

## Prerequisites

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, set up and use BuildKit directly, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/build-environments` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/build-environments/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

## Deployment Workflow

### Package the base image

Package and push the base Go runtime image (see `server.go` for the runtime implementation):

```bash title="unikraft"
unikraft build . --output <my-org>/go-build-env:latest
```

The server in [`server.go`](./server.go) loads `/rom/rom.go`, compiles it to `/run/rom.so` using `go build -buildmode=plugin`, and invokes `Handler()` from the plugin.

### Create an instance template from the base image

Create a short-lived instance from the base image (without ROM attached).
The server writes to `/uk/libukp/template_instance` and turns the instance into a template before serving requests (see https://unikraft.com/docs/platform/instances#instance-templates):

```bash title="unikraft"
unikraft run --metro fra \
  --name go-build-env \
  -m 512M \
  --image <my-org>/go-build-env:latest
```

The output shows the instance details:

```ansi title="unikraft"
metro:        fra
name:         go-build-env
uuid:         650dbbe7-3949-4c93-88e7-6619a9216e0c
state:        starting
image:        <my-org>/go-build-env
resources:
  memory:     512MiB
  vcpus:      1
networks:
- uuid:       6f7a8b9c-0d1e-2f3a-4b5c-f6a7b8c9d0e1
  private-ip: 10.0.5.4
  mac:        12:b0:6c:3e:ab:95
timestamps:
  created:    just now
```

If you are fast enough, you can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

This instance is short-lived, since right before the server starts, it triggers a conversion into a template.
To check the template is ready, run:

```bash title="unikraft"
unikraft instances templates list
```

```ansi title="unikraft"
METRO  NAME          STATE     IMAGE                  ARGS  MEMORY  VCPUS  CREATED
fra    go-build-env  template  <my-org>/go-build-env        512MiB  1      2 minutes ago
```

### Package the ROMs

Each ROM contains a Go function implementation (see [`rom1/fs/rom.go`](./rom1/fs/rom.go) and [`rom2/fs/rom.go`](./rom2/fs/rom.go)).

```bash title="unikraft"
unikraft build rom1/ --output <my-org>/go-rom1:latest
unikraft build rom2/ --output <my-org>/go-rom2:latest
```

### Create instances from the template with different ROMs attached

Create an instance with the first ROM:

```bash title="unikraft"
unikraft run --metro fra \
  --name go-build-env-rom1 \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000,stateful=true \
  --rom image=<my-org>/go-rom1:latest,at=/rom \
  --template go-build-env
```

The instance will compile the ROM into a plugin on first start, which may take a few seconds.
To check the progress, you can view the instance logs:

```bash title="unikraft"
unikraft instances logs go-build-env-rom1 -f
```

Create another instance with the second ROM:

```bash title="unikraft"
unikraft run --metro fra \
  --name go-build-env-rom2 \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000,stateful=true \
  --rom image=<my-org>/go-rom2:latest,at=/rom \
  --template go-build-env
```

The instance will compile the ROM into a plugin on first start, which may take a few seconds.
To check the progress, you can view the instance logs:

```bash title="unikraft"
unikraft instances logs go-build-env-rom2 -f
```

List the instances and note their FQDN values:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME               STATE    IMAGE                  ARGS  MEMORY  VCPUS  FQDN                                      CREATED
fra    go-build-env-rom2  standby  <my-org>/go-build-env        512MiB  1      nameless-wood-gw7pbnls.fra.unikraft.app   2 minutes ago
fra    go-build-env-rom1  standby  <my-org>/go-build-env        512MiB  1      sparkling-dawn-syowlbtj.fra.unikraft.app  3 minutes ago
```

Test both instances:

```bash
curl https://sparkling-dawn-syowlbtj.fra.unikraft.app
curl https://nameless-wood-gw7pbnls.fra.unikraft.app
```

```text
Bye, World!
Auf Wiedersehen!
```

## Cleanup

```bash title="unikraft"
unikraft instances delete go-build-env-rom1 go-build-env-rom2
unikraft instances template delete go-build-env
```

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
