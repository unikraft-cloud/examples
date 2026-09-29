# Erlang HTTP Server

This guide explains how to create and deploy a simple Erlang-based HTTP web server.
To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-erlang26.2/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-erlang26.2/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-erlang262:latest
unikraft run --metro fra \
  -m 512M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=idle,cooldown-time=1000,stateful=true \
  --image <my-org>/httpserver-erlang262:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         httpserver-erlang262-sw2bp
uuid:         1c4a8a51-fb61-45fc-87b8-26d192a7c2bc
state:        starting
image:        <my-org>/httpserver-erlang262
resources:
  memory:     512MiB
  vcpus:      1
service:
  uuid:       c7a6b443-c424-8a96-ce90-e833841b6eca
  name:       patient-field-ck629j2u
  domains:
  - fqdn:     patient-field-ck629j2u.fra.unikraft.app
networks:
- uuid:       6d767165-9196-e27d-bb12-5eb5a9188654
  private-ip: 10.0.3.3
  mac:        12:b0:05:ce:23:30
timestamps:
  created:    just now
```

In this case, the instance name is `httpserver-erlang262-sw2bp` and the address is `https://patient-field-ck629j2u.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Erlang-based HTTP web server:

```bash
curl https://patient-field-ck629j2u.fra.unikraft.app
```

```text
Hello, World!
```

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                        STATE    IMAGE                          ARGS  MEMORY  VCPUS  FQDN                                     CREATED
fra    httpserver-erlang262-sw2bp  running  <my-org>/httpserver-erlang262        512MiB  1      patient-field-ck629j2u.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete httpserver-erlang262-sw2bp
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `http_server.erl`: the actual Erlang HTTP server implementation
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

The following options are available for customizing the app:

* If you only update the implementation in the `http_server.erl` source file, you don't need to make any other changes.

* If you create any new source files, copy them into the app filesystem by using the `COPY` command in the `Dockerfile`.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
