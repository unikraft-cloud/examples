# Serverless Functions: Node.js Code Execution with ROMs

Serverless functions let you deploy small pieces of business logic without managing servers or runtimes.
This example implements that model for Node.js, keeping the function code separate from the runtime image that executes it, so you update a function without rebuilding the runtime.

This guide explains how to deploy TypeScript/JavaScript functions as auxiliary Read-Only Memory (ROM) images, then load them dynamically in a Node.js runtime.
With Unikraft Cloud, you can create a base image with a generic runtime, package custom code as ROMs, and attach different ROMs to instances of the same base image.

## Prerequisites

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, set up and use BuildKit directly, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/node-code-execution` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/node-code-execution/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

## Deployment Workflow

### Package the base image

First, package and push the base Node.js image (see `server.ts` for the runtime implementation):

```bash title="unikraft"
unikraft build . --output <my-org>/node-code-exec:latest
```

The server implementation in `server.ts` is a simple Node.js application that listens for HTTP requests and executes JavaScript code from the attached ROM, if available.
There is a little tweak—right before loading the ROM code and starting the server, it writes `1` to the special file `/uk/libukp/template_instance` (see https://unikraft.com/docs/platform/instances#instance-templates), triggering a conversion of the instance into a template.

### Create an instance template from the base image

Create an instance that uses the base Node.js image without any ROM attached:

```bash title="unikraft"
unikraft run --metro fra \
  --name node-exec \
  -m 512M \
  --image <my-org>/node-code-exec:latest
```

The output shows the instance details:

```ansi title="unikraft"
metro:        fra
name:         node-exec
uuid:         96608ed2-45e0-4c8f-8269-5d8cd3e4b41a
state:        starting
image:        <my-org>/node-code-exec
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

This instance is short-lived, since right before the server starts, it triggers a conversion into a template.
To check that the template is ready, run:

```bash title="unikraft"
unikraft instances templates list
```

```ansi title="unikraft"
METRO  NAME       STATE     IMAGE                    ARGS  MEMORY  VCPUS  CREATED
fra    node-exec  template  <my-org>/node-code-exec        512MiB  1      5 seconds ago
```

### Package the ROMs

Create and push the ROMs with the code (see `rom1/fs/rom.js` and `rom2/fs/rom.ts`):

```bash title="unikraft"
unikraft build rom1/ --output <my-org>/node-rom1:latest
unikraft build rom2/ --output <my-org>/node-rom2:latest
```

### Create instances from the template with different ROMs attached

Create a new instance from the template, attaching the first ROM:

```bash title="unikraft"
unikraft run --metro fra \
  --name node-exec-rom1 \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000,stateful=true \
  --rom image=<my-org>/node-rom1:latest,at=/rom \
  --template node-exec
```

Create another instance from the same template, but with the second ROM attached:

```bash title="unikraft"
unikraft run --metro fra \
  --name node-exec-rom2 \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000,stateful=true \
  --rom image=<my-org>/node-rom2:latest,at=/rom \
  --template node-exec
```

List the instances and note their FQDN values:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME            STATE    IMAGE                    ARGS  MEMORY  VCPUS  FQDN                                      CREATED
fra    node-exec-rom2  standby  <my-org>/node-code-exec        512MiB  1      nameless-wood-gw7pbnls.fra.unikraft.app   2 minutes ago
fra    node-exec-rom1  standby  <my-org>/node-code-exec        512MiB  1      sparkling-dawn-syowlbtj.fra.unikraft.app  3 minutes ago
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

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
