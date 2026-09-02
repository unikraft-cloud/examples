# Serverless Functions: Node.js Code Execution with ROMs

Serverless functions let you deploy small pieces of business logic without managing servers or runtimes.
This example implements that model for Node.js, keeping the function code separate from the runtime image that executes it, so you update a function without rebuilding the runtime.

This guide explains how to deploy TypeScript/JavaScript functions as auxiliary Read-Only Memory (ROM) images, then load them dynamically in a Node.js runtime.
With Unikraft Cloud, you can create a base image with a generic runtime, package custom code as ROMs, and attach different ROMs to instances of the same base image.

## Prerequisites

1. Install the CLI:
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, set up and use BuildKit directly, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/node-code-execution` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/node-code-execution/
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
export UKC_METRO=fra
```

## Deployment Workflow

### Package the base image

First, package and push the base Node.js image (see `server.ts` for the runtime implementation):

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft build . --output <my-org>/node-code-exec:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft pkg \
  --name index.unikraft.io/<my-org>/node-code-exec:latest \
  --plat kraftcloud \
  --arch x86_64 \
  --rootfs-type erofs \
  --push \
  .
```

The server implementation in `server.ts` is a simple Node.js application that listens for HTTP requests and executes JavaScript code from the attached ROM, if available.
There is a little tweak—right before loading the ROM code and starting the server, it writes `1` to the special file `/uk/libukp/template_instance` (see https://unikraft.com/docs/platform/instances#instance-templates), triggering a conversion of the instance into a template.

### Create an instance template from the base image

Create an instance that uses the base Node.js image without any ROM attached:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft run --metro fra \
  --name node-exec \
  -m 512M \
  --image <my-org>/node-code-exec:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance create \
  --start \
  --name node-exec \
  -M 512Mi \
  <my-org>/node-code-exec:latest
```

The output shows the instance details:

**Using the unikraft CLI (Recommended)**
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

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: node-exec
 ├───────── uuid: 96608ed2-45e0-4c8f-8269-5d8cd3e4b41a
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├──────── image: oci://unikraft.io/<my-org>/node-code-exec@sha256:71487fd6196987cf65fb89eb84405cb796677aba177dabacf391f09618313328
 ├─────── memory: 512 MiB
 ├─ private fqdn: node-exec.internal
 └─── private ip: 10.0.5.4
```

This instance is short-lived, since right before the server starts, it triggers a conversion into a template.
To check that the template is ready, run:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances templates list
```

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
METRO  NAME       STATE     IMAGE                    ARGS  MEMORY  VCPUS  CREATED
fra    node-exec  template  <my-org>/node-code-exec        512MiB  1      5 seconds ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance template list
```

**Using the legacy kraft CLI**
```bash title="kraft"
NAME       IMAGE                                                                                                              ARGS  CREATED AT
node-exec  oci://unikraft.io/<my-org>/node-code-exec@sha256:71487fd6196987cf65fb89eb84405cb796677aba177dabacf391f09618313328        5 seconds ago
```

### Package the ROMs

Create and push the ROMs with the code (see `rom1/fs/rom.js` and `rom2/fs/rom.ts`):

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft build rom1/ --output <my-org>/node-rom1:latest
unikraft build rom2/ --output <my-org>/node-rom2:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft pkg \
  --name index.unikraft.io/<my-org>/node-rom1:latest \
  --rom ./fs \
  --rom-type erofs \
  --plat kraftcloud \
  --arch x86_64 \
  --push \
  rom1/
kraft pkg \
  --name index.unikraft.io/<my-org>/node-rom2:latest \
  --rom ./fs \
  --rom-type erofs \
  --plat kraftcloud \
  --arch x86_64 \
  --push \
  rom2/
```

### Create instances from the template with different ROMs attached

Create a new instance from the template, attaching the first ROM:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft run --metro fra \
  --name node-exec-rom1 \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000,stateful=true \
  --rom image=<my-org>/node-rom1:latest,at=/rom \
  --template node-exec
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
# kraft does not support creating instances with attached ROMs, but you can use the API directly
curl -X POST "$UKC_METRO/instances" \
   -H "Accept: application/json" \
   -H "Authorization: Bearer $UKC_TOKEN" \
   -H "Content-Type: application/json" \
   -d '{
   "name": "node-exec-rom1",
   "template": {
      "name": "node-exec"
   },
   "autostart": true,
   "service_group": {
      "services": [
         {
            "port": 443,
            "destination_port": 8080,
            "handlers": ["tls", "http"]
         }
      ]
   },
   "scale_to_zero": {
      "policy": "on",
      "stateful": true,
      "cooldown_time_ms": 1000
   },
   "roms": [
      {
         "name": "js_function",
         "image": "index.unikraft.io/<my-org>/node-rom1:latest",
         "at": "/rom"
      }
   ]
}'
```

Create another instance from the same template, but with the second ROM attached:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft run --metro fra \
  --name node-exec-rom2 \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000,stateful=true \
  --rom image=<my-org>/node-rom2:latest,at=/rom \
  --template node-exec
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
# kraft does not support creating instances with attached ROMs, but you can use the API directly
curl -X POST "$UKC_METRO/instances" \
   -H "Accept: application/json" \
   -H "Authorization: Bearer $UKC_TOKEN" \
   -H "Content-Type: application/json" \
   -d '{
   "name": "node-exec-rom2",
   "template": {
      "name": "node-exec"
   },
   "autostart": true,
   "service_group": {
      "services": [
         {
            "port": 443,
            "destination_port": 8080,
            "handlers": ["tls", "http"]
         }
      ]
   },
   "scale_to_zero": {
      "policy": "on",
      "stateful": true,
      "cooldown_time_ms": 1000
   },
   "roms": [
      {
         "name": "ts_function",
         "image": "index.unikraft.io/<my-org>/node-rom2:latest",
         "at": "/rom"
      }
   ]
}'
```

List the instances and note their FQDN values:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```bash title="unikraft"
METRO  NAME            STATE    IMAGE                    ARGS  MEMORY  VCPUS  FQDN                                      CREATED
fra    node-exec-rom2  standby  <my-org>/node-code-exec        512MiB  1      nameless-wood-gw7pbnls.fra.unikraft.app   2 minutes ago
fra    node-exec-rom1  standby  <my-org>/node-code-exec        512MiB  1      sparkling-dawn-syowlbtj.fra.unikraft.app  3 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```bash title="kraft"
NAME            FQDN                                      STATE    STATUS   IMAGE                                                       MEMORY   VCPUS  ARGS  BOOT TIME
node-exec-rom2  nameless-wood-gw7pbnls.fra.unikraft.app   standby  standby  oci://unikraft.io/<my-org>/node-code-exec@sha256:71487f...  512 MiB  1            6.98 ms
node-exec-rom1  sparkling-dawn-syowlbtj.fra.unikraft.app  standby  standby  oci://unikraft.io/<my-org>/node-code-exec@sha256:71487f...  512 MiB  1            7.86 ms
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
