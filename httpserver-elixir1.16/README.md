# Elixir HTTP Server

This guide explains how to create and deploy a simple Elixir-based HTTP web server.
To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-elixir1.16/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-elixir1.16/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-elixir116:latest
unikraft run --metro fra \
  -m 1G \
  -p 443:3000/tls+http \
  --scale-to-zero policy=idle,cooldown-time=3000,stateful=true \
  --image <my-org>/httpserver-elixir116:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         httpserver-elixir116-qo9k3
uuid:         e5fbf089-b000-4b2d-a827-44a1f5d28f24
state:        starting
image:        <my-org>/httpserver-elixir116
resources:
  memory:     1024MiB
  vcpus:      1
service:
  uuid:       ddbc554c-3ce1-01ea-27d9-61690cb85717
  name:       small-water-tl8lr8am
  domains:
  - fqdn:     small-water-tl8lr8am.fra.unikraft.app
networks:
- uuid:       4e9f6ce2-9f8d-04ed-35e8-073582ac66bc
  private-ip: 10.0.3.4
  mac:        12:b0:a2:d1:d5:d4
timestamps:
  created:    just now
```

In this case, the instance name is `httpserver-elixir116-qo9k3` and the address is `https://small-water-tl8lr8am.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Elixir-based HTTP web server:

```bash
curl https://small-water-tl8lr8am.fra.unikraft.app
```

```text
Hello, World!
```

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                        STATE    IMAGE                          ARGS  MEMORY  VCPUS  FQDN                                   CREATED
fra    httpserver-elixir116-qo9k3  running  <my-org>/httpserver-elixir116        1.0GiB  1      small-water-tl8lr8am.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete httpserver-elixir116-qo9k3
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `lib/`, `mix.exs`: the actual Elixir HTTP server implementation
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

The following options are available for customizing the app:

* If you only update the implementation in the `lib/server.ex` or `lib/server/app.ex` source code files, no other changes apply.
  If you add new source files in the `lib/` directory, you don't need to make any other changes.

* If you create any new source files, copy them into the app filesystem by using the `COPY` command in the `Dockerfile`.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

The following commands generate the current source code files and configuration file (`mix.exs`):

```console
mix new --app server . --sup
```

Use a similar command to create a new app.
Then update it and deploy it on Unikraft Cloud using the above instructions.

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
