# Spin

This guide explains how to create and deploy a simple Spin HTTP app.
This guide comes from  [Spin's `spin-wagi-http` example](https://github.com/fermyon/spin/tree/v2.1.0/examples/spin-wagi-http).
It shows how to run a Spin app serving routes from two programs written in different languages (Rust and C++).

To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

> **Note**:
> The unikraft CLI is the current standard, while kraft is the legacy version.
> Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/spin-wagi-http/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/spin-wagi-http/
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
unikraft build . --output <my-org>/spin-wagi-http:latest
unikraft run --scale-to-zero policy=on,cooldown-time=1000,stateful=true --metro fra -p 443:3000/tls+http -m 4G --image <my-org>/spin-wagi-http:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy --scale-to-zero on --scale-to-zero-stateful --scale-to-zero-cooldown 1s -p 443:3000/tls+http -M 4Gi .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         spin-wagi-http-is72r
uuid:         045c1bda-0f2e-4f8b-98c7-a208bfa7d143
state:        starting
image:        <my-org>/spin-wagi-http
resources:
  memory:     4096MiB
  vcpus:      1
service:
  uuid:       9b5b88fd-16ce-3db6-a828-ee885647d820
  name:       damp-bobo-wg43p36e
  domains:
  - fqdn:     damp-bobo-wg43p36e.fra.unikraft.app
networks:
- uuid:       db3851f6-ace1-8601-b6fa-925b7fdf8390
  private-ip: 10.0.28.16
  mac:        12:b0:fc:f5:09:d5
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: spin-wagi-http-is72r
 ├───────── uuid: 045c1bda-0f2e-4f8b-98c7-a208bfa7d143
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://damp-bobo-wg43p36e.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/spin-wagi-http@sha256:57a5151996d83332af6da521e1cd92271a8c3ac7ae26bc44a7c0dbbc0a30e577
 ├─────── memory: 4096 MiB
 ├────── service: damp-bobo-wg43p36e
 ├─ private fqdn: spin-wagi-http-is72r.internal
 └─── private ip: 10.0.28.16
```

In this case, the instance name is `spin-wagi-http-is72r` and the address is `https://damp-bobo-wg43p36e.fra.unikraft.app`.
They're different for each run.

Then `curl` the hello route:

```bash
curl -i https://damp-bobo-wg43p36e.fra.unikraft.app/hello

Hello, Fermyon!
```

And `curl` the goodbye route:

```bash
curl -i https://damp-bobo-wg43p36e.fra.unikraft.app/goodbye

Goodbye, Fermyon!
```

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                  STATE    IMAGE                    ARGS  MEMORY  VCPUS  FQDN                                 CREATED
fra    spin-wagi-http-is72r  running  <my-org>/spin-wagi-http        4.0GiB  1      damp-bobo-wg43p36e.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                  FQDN                                 STATE    STATUS        IMAGE                                              MEMORY   VCPUS  ARGS  BOOT TIME
spin-wagi-http-is72r  damp-bobo-wg43p36e.fra.unikraft.app  running  1 minute ago  oci://unikraft.io/<my-org>/spin-wagi-http@sha2...  4.0 GiB  1            300.06 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete spin-wagi-http-is72r
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove spin-wagi-http-is72r
```

## Compare boot times (cold vs warm)

The `compare-boot.sh` script benchmarks cold boot (Spin starts from a published
image and instantiates both wasm components) against warm restore (a snapshot
template, where Spin is already running and the wasm modules are pre-loaded).

Edit `config` once to point at your registry org:

```sh
IMAGE_NAME="spin-wagi-http"
BASE_IMAGE="<your-org>/spin-wagi-http"
INSTANCE_NAME="spin-wagi-http-1"
MEMORY_MB="4096"
```

Then `source ./config` so the variables are exported for the commands below.

### How the snapshot is triggered

This image's entrypoint is a tiny static Go binary at `/launcher` (see
[`launcher/launcher.go`](./launcher/launcher.go)) that:

1. Execs `spin up ...` with the args from the Kraftfile.
2. Polls `127.0.0.1:3000` until Spin's HTTP listener is bound.
3. If `TEMPLATE=1` is set, writes `1` to `/uk/libukp/template_instance`.
   That write is what tells Unikraft Cloud to snapshot the running instance
   and promote it to a template — Spin and both wasm components are part of
   the snapshot.

Spin itself has no concept of the UKC magic file, so the wrapper is what
bridges the two.

### 1. Build & push

```sh
unikraft build . --output "index.unikraft.io/${BASE_IMAGE}:latest"
```

### 2. Create the template

```sh
unikraft run \
    --name "${INSTANCE_NAME}-tpl" \
    --image "index.unikraft.io/${BASE_IMAGE}:latest" \
    --memory "${MEMORY_MB}MiB" \
    --autostart \
    --restart never \
    --scale-to-zero policy=off \
    -e TEMPLATE=1 \
    -p 443:3000/tls+http
```

### 3. Run the benchmark

```sh
./compare-boot.sh        # 3 cold + 3 warm (default)
./compare-boot.sh 5      # 5 of each
./compare-boot.sh 50     # 50 of each
```

The script spawns N instances from the image and N from the template, then
prints summary statistics (count/min/max/mean/median) of `timing.boot-time`
for each group before cleaning up. Warm instances are spawned with
scale-to-zero on so the demo also exercises the network-triggered wake path.

Example run with 50 of each:

```text
==> Booting 50 cold + 50 warm instances...
==> Waiting for instances to finish booting...

==> Cold-boot (from image) — 50 instances
  count : 50
  min   : 244.817 ms
  max   : 329.338 ms
  mean  : 277.214 ms
  median: 266.058 ms

==> Warm-boot (from template) — 50 instances
  count : 50
  min   : 5.724 ms
  max   : 10.059 ms
  mean  : 6.400 ms
  median: 6.282 ms
```

Warm restore from a template is roughly **40× faster** than a cold boot here
(~6 ms vs ~277 ms mean), since Spin and both wasm components are already
resident in the snapshot.

## Customize your app

To customize the app, update the files in the repository, listed below:

* `wagi-http-cpp`: C++ server handling the hello route
* `http-rust`: Rust server handling the goodbye route
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem
* `spin.toml`: The Spin TOML configuration file

Lines in the `Kraftfile` have the following roles:

* `spec: v0.7`: The current `Kraftfile` specification version is `0.7`.

* `runtime: base-compat:latest`: The runtime kernel to use is the base compatibility kernel.

* `rootfs`: Build the app root filesystem.
  `source: ./Dockerfile` means the filesystem is built using the `Dockerfile`.
  `format: erofs` means the filesystem type is [EROFS](https://erofs.docs.kernel.org/).

* `cmd: ["/usr/bin/spin", "up", "--from", "/app/spin.toml", "--listen", "0.0.0.0:3000"]`: Use `spin` as the command to start the app, with the given parameters.

The following options are available for customizing the app:

* If only updating the existing files under the `wagi-http-cpp` and `http-rust` directories, you don't need to make any other changes.

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
