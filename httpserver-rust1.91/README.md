# Rust HTTP Server

This guide explains how to create and deploy a Rust app.
To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-rust1.91` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-rust1.91/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-rust191:latest
unikraft run --metro fra \
  -m 384M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/httpserver-rust191:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         httpserver-rust191-pinzf
uuid:         8acb3d35-38ba-4929-81de-950340662c14
state:        starting
image:        <my-org>/httpserver-rust191
resources:
  memory:     384MiB
  vcpus:      1
service:
  uuid:       3bf42986-3032-1ff2-fe4d-2041db03b628
  name:       snowy-feather-k4pfgl8t
  domains:
  - fqdn:     snowy-feather-k4pfgl8t.fra.unikraft.app
networks:
- uuid:       d64344f4-e159-c7c3-7f1b-ba10bcc60f67
  private-ip: 10.0.2.53
  mac:        12:b0:1d:12:0e:46
timestamps:
  created:    just now
```

In this case, the instance name is `httpserver-rust191-pinzf` and the address is `snowy-feather-k4pfgl8t.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance:

```bash
curl https://snowy-feather-k4pfgl8t.fra.unikraft.app
```

```text
Hello, World!
```

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                      STATE    IMAGE                        ARGS  MEMORY  VCPUS  FQDN                                     CREATED
fra    httpserver-rust191-pinzf  standby  <my-org>/httpserver-rust191        384MiB  1      snowy-feather-k4pfgl8t.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete httpserver-rust191-pinzf
```

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
