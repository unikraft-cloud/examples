# Rust (Actix Web) HTTP Server

This example uses [`actix-web`](https://actix.rs), a popular Rust web framework.
To run it, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

1. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-rust1.88-actix-web4/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-rust1.88-actix-web4/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-rust188-actix-web4:latest
unikraft run --metro fra \
  -m 256M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/httpserver-rust188-actix-web4:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         httpserver-rust188-actix-web4-3pj27
uuid:         3e729de6-a1fb-5818-63d4-51a905fa6a5d
state:        starting
image:        <my-org>/httpserver-rust188-actix-web4
resources:
  memory:     256MiB
  vcpus:      1
service:
  uuid:       bf564711-3ec0-be8c-64ca-e27c5034d3fe
  name:       autumn-silence-wupu2nus
  domains:
  - fqdn:     autumn-silence-wupu2nus.fra.unikraft.app
networks:
- uuid:       53417e5b-ae43-6307-d433-9a22c0d249a9
  private-ip: 10.0.3.3
  mac:        12:b0:58:9f:9e:51
timestamps:
  created:    just now
```

In this case, the instance name is `httpserver-rust188-actix-web4-3pj27` and the address is `https://autumn-silence-wupu2nus.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Rust-based HTTP web server:

```bash
curl https://autumn-silence-wupu2nus.fra.unikraft.app
curl https://autumn-silence-wupu2nus.fra.unikraft.app/hey
```

```text
Hello, World!
Hey there!
```

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                                 STATE    IMAGE                                   ARGS  MEMORY  VCPUS  FQDN                                      CREATED
fra    httpserver-rust188-actix-web4-3pj27  running  <my-org>/httpserver-rust188-actix-web4        256MiB  1      autumn-silence-wupu2nus.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete httpserver-rust188-actix-web4-3pj27
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
