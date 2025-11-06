# Rust (Rocket)

This example uses [`Rocket`](https://rocket.rs/), a popular Rust web framework.
To run this example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/http-rust1.75-rocket0.5/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/http-rust1.75-rocket0.5
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
 ├────────── name: http-rust175-rocket05-tuwq3
 ├────────── uuid: b6fe13e4-93b7-402b-bdec-1bc4d81bc275
 ├───────── state: running
 ├─────────── url: https://empty-bobo-n3htmpye.fra.unikraft.app
 ├───────── image: http-rust175-rocket05@sha256:23a7a6e155758e6e8f75e9570f0aec5fb744f08c1bad2454d7386367c5ea45d6
 ├───── boot time: 17.41 ms
 ├──────── memory: 128 MiB
 ├─────── service: empty-bobo-n3htmpye
 ├── private fqdn: http-rust175-rocket05-tuwq3.internal
 ├──── private ip: 172.16.6.6
 └────────── args: /server
```

In this case, the instance name is `http-rust175-rocket05-tuwq3` and the address is `https://empty-bobo-n3htmpye.fra.unikraft.app`.
They're different for each run.

Use `curl` to query any of the Rocket server's paths, for example:

```bash
curl https://empty-bobo-n3htmpye.fra.unikraft.app/wave/Rocketeer/100
```
```text
👋 Hello, 100 year old named Rocketeer!
```

You can list information about the instance by running:

```bash
kraft cloud instance list
```
```ansi
NAME                         FQDN                                  STATE    STATUS        IMAGE                                   MEMORY   VCPUS  ARGS     BOOT TIME
http-rust175-rocket05-tuwq3  empty-bobo-n3htmpye.fra.unikraft.app  running  1 minute ago  http-rust175-rocket05@sha256:23a7a6...  128 MiB  1      /server  17412us
```

When done, you can remove the instance:

```bash
kraft cloud instance remove http-rust175-rocket05-tuwq3
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `src/main.rs`: the actual server
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
