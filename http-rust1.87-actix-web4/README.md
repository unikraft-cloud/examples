# Rust (Actix Web)

This example uses [`actix-web`](https://actix.rs), a popular Rust web framework.
To run this example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

1. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/http-rust1.87-actix-web4/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/http-rust1.87-actix-web4/
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
kraft cloud deploy -p 443:8080 .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: http-rust187-actix-web4-3pj27
 ├────────── uuid:33e9b4ba-58d7-4b3a-b9dd-4c406c0e7b07
 ├───────── state: running
 ├─────────── url: https://autumn-silence-wupu2nus.fra.unikraft.app
 ├───────── image: http-rust187-actix-web4@sha256:11723705230f0f4545d2be7e4867dc67b396870769e91f05e2fa6d9da94f9b59
 ├───── boot time: 11.67 ms
 ├──────── memory: 128 MiB
 ├─────── service: autumn-silence-wupu2nus
 ├── private fqdn: http-rust187-actix-web4-3pj27.internal
 ├──── private ip: 172.16.3.3
 └────────── args: /server
```

In this case, the instance name is `http-rust187-actix-web4-3pj27` and the address is `https://autumn-silence-wupu2nus.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Rust-based HTTP web server:

```bash
curl https://autumn-silence-wupu2nus.fra.unikraft.app
curl https://autumn-silence-wupu2nus.fra.unikraft.app/hey
```
```text
Hello world!
Hey there!
```

You can list information about the instance by running:

```bash
kraft cloud instance list
```
```ansi
NAME                           FQDN                                      STATE    STATUS          IMAGE                                                      MEMORY   VCPUS  ARGS     BOOT TIME
http-rust187-actix-web4-3pj27  autumn-silence-wupu2nus.fra.unikraft.app  running  10 minutes ago  http-rust187-actix-web4@sha256:11723705230f0f4545d2be7...  128 MiB  1      /server  11672us
```

When done, you can remove the instance:

```bash
kraft cloud instance remove http-rust187-actix-web4-3pj27
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `src/main.rs`: the actual implementation
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

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
