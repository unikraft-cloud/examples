# Spin

This guide explains how to create and deploy a simple Spin HTTP app.
This guide comes from  [Spin's `spin-wagi-http` example](https://github.com/fermyon/spin/tree/v2.1.0/examples/spin-wagi-http).
It shows how to run a Spin app serving routes from two programs written in different languages (Rust and C++).

To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

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

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/spin-wagi-http:latest
unikraft run --metro fra \
  -m 4G \
  -p 443:3000/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000,stateful=true \
  --image <my-org>/spin-wagi-http:latest
```

The output shows the instance address and other details:

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

```ansi title="unikraft"
METRO  NAME                  STATE    IMAGE                    ARGS  MEMORY  VCPUS  FQDN                                 CREATED
fra    spin-wagi-http-is72r  running  <my-org>/spin-wagi-http        4.0GiB  1      damp-bobo-wg43p36e.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete spin-wagi-http-is72r
```

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

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
