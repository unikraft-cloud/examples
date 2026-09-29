# Rust (Rocket) HTTP Server

This example uses [`Rocket`](https://rocket.rs/), a popular Rust web framework.
To run it, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-rust1.88-rocket0.5/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-rust1.88-rocket0.5
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-rust188-rocket05:latest
unikraft run --metro fra \
  -m 256M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/httpserver-rust188-rocket05:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         httpserver-rust188-rocket05-tuwq3
uuid:         b6fe13e4-93b7-402b-bdec-1bc4d81bc275
state:        starting
image:        <my-org>/httpserver-rust188-rocket05
resources:
  memory:     256MiB
  vcpus:      1
service:
  uuid:       57da8f4a-5c68-3d4c-3b8f-987ee2ba0fb3
  name:       empty-bobo-n3htmpye
  domains:
  - fqdn:     empty-bobo-n3htmpye.fra.unikraft.app
networks:
- uuid:       fb33101e-f3b6-0859-38b9-71fb057cab4a
  private-ip: 10.0.6.6
  mac:        12:b0:07:e5:d1:fe
timestamps:
  created:    just now
```

In this case, the instance name is `httpserver-rust188-rocket05-tuwq3` and the address is `https://empty-bobo-n3htmpye.fra.unikraft.app`.
They're different for each run.

Use `curl` to query any of the Rocket server's paths, for example:

```bash
curl https://empty-bobo-n3htmpye.fra.unikraft.app/wave/Rocketeer/100
```

```text
👋 Hello, 100 year old named Rocketeer!
```

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                               STATE    IMAGE                                 ARGS  MEMORY  VCPUS  FQDN                                  CREATED
fra    httpserver-rust188-rocket05-tuwq3  running  <my-org>/httpserver-rust188-rocket05        256MiB  1      empty-bobo-n3htmpye.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete httpserver-rust188-rocket05-tuwq3
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `src/main.rs`: the actual server implementation
* `Cargo.toml`: the Cargo package manager configuration file
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

The following options are available for customizing the app:

* If you only update the implementation in the `src/main.rs` source file, you don't need to make any other changes.

* If you create any new source files, copy them into the app filesystem by using the `COPY` command in the `Dockerfile`.
  If you add new Rust source code files, be sure to configure required dependencies in the `Cargo.toml` file.

* If you build a new executable, update the `cmd` line in the `Kraftfile` and replace `/server` with the path to the new executable.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
