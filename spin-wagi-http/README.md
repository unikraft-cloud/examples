# Spin

This guide explains how to create and deploy a simple Spin HTTP app.
This guide comes from  [Spin's `spin-wagi-http` example](https://github.com/fermyon/spin/tree/v2.1.0/examples/spin-wagi-http).
It shows how to run a Spin app serving routes from two programs written in different languages (Rust and C++).
Both the Spin executor and the Wagi executor on Unikraft Cloud.
To run it, follow these steps:

1. Install the CLI and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/spin-wagi-http/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/spin-wagi-http/
```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

or

```bash title="kraft"
# Set Unikraft Cloud access token
export UKC_TOKEN=token
# Set metro to Frankfurt, DE
export UKC_METRO=fra
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/spin-wagi-http:latest
unikraft run --metro fra -p 443:3000/tls+http -m 4G --image <my-org>/spin-wagi-http:latest
```

or

```bash title="kraft"
kraft cloud deploy -p 443:3000/tls+http -M 4G .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: spin-wagi-http-is72r
 ├────────── uuid: 045c1bda-0f2e-4f8b-98c7-a208bfa7d143
 ├───────── state: running
 ├─────────── url: https://damp-bobo-wg43p36e.fra.unikraft.app
 ├───────── image: spin-wagi-http@sha256:57a5151996d83332af6da521e1cd92271a8c3ac7ae26bc44a7c0dbbc0a30e577
 ├───── boot time: 300.06 ms
 ├──────── memory: 4096 MiB
 ├─────── service: damp-bobo-wg43p36e
 ├── private fqdn: spin-wagi-http-is72r.internal
 ├──── private ip: 172.16.28.16
 └────────── args: /usr/bin/spin up --from /app/spin.toml --listen 0.0.0.0:3000
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

```bash title="unikraft"
unikraft instances list
```

or

```bash title="kraft"
kraft cloud instance list
```

```ansi
NAME                  FQDN                                 STATE    STATUS        IMAGE                   MEMORY   VCPUS  ARGS                                      BOOT TIME
spin-wagi-http-is72r  damp-bobo-wg43p36e.fra.unikraft.app  running  1 minute ago  spin-wagi-http@sha2...  4.0 GiB  1      /usr/bin/spin up --from /app/spin.tom...  300064us
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete spin-wagi-http-is72r
```

or

```bash title="kraft"
kraft cloud instance remove spin-wagi-http-is72r
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `wagi-http-cpp`: C++ server handling the hello route
* `http-rust`: Rust server handling the goodbye route
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem
* `spin.toml`: The Spin TOML configuration file

Lines in the `Kraftfile` have the following roles:

* `spec: v0.6`: The current `Kraftfile` specification version is `0.6`.

* `runtime: base-compat:latest`: The runtime kernel to use is the base compatibility kernel.

* `rootfs`: Build the app root filesystem.
  `source: ./Dockerfile` means the filesystem is built using the `Dockerfile`.
  `type: erofs` means the filesystem type is [EROFS](https://erofs.docs.kernel.org/).

* `cmd: ["/usr/bin/spin", "up", "--from", "/app/spin.toml", "--listen", "0.0.0.0:3000"]`: Use `spin` as the command to start the app, with the given parameters.

The following options are available for customizing the app:

* If only updating the existing files under the `wagi-http-cpp` and `http-rust` directories, you don't need to make any other changes.

* If you create any new source files, copy them into the app filesystem by using the `COPY` command in the `Dockerfile`.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

or

```bash title="kraft"
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft) or the [legacy CLI Reference](https://unikraft.com/docs/cli/kraft/overview).
