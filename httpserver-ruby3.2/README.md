# Ruby HTTP Server

This guide explains how to create and deploy a simple Ruby-based HTTP web server.
To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-ruby3.2/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-ruby3.2/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-ruby32:latest
unikraft run --metro fra \
  -m 256M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/httpserver-ruby32:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         httpserver-ruby32-s6l8n
uuid:         b1ebbbc0-5efa-476c-adb6-99866773245c
state:        starting
image:        <my-org>/httpserver-ruby32
resources:
  memory:     256MiB
  vcpus:      1
service:
  uuid:       bcc07c7c-9289-11f4-6e3d-8f7fdde45256
  name:       silent-resonance-1jtz5c66
  domains:
  - fqdn:     silent-resonance-1jtz5c66.fra.unikraft.app
networks:
- uuid:       50203783-cf51-81d1-aa2d-615f939043af
  private-ip: 10.0.3.3
  mac:        12:b0:0a:4f:7a:84
timestamps:
  created:    just now
```

In this case, the instance name is `httpserver-ruby32-s6l8n` and the address is `https://silent-resonance-1jtz5c66.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Ruby-based HTTP web server:

```bash
curl https://silent-resonance-1jtz5c66.fra.unikraft.app
```

```text
Hello, World!
```

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                     STATE    IMAGE                       ARGS  MEMORY  VCPUS  FQDN                                    CREATED
fra    httpserver-ruby32-s6l8n  running  <my-org>/httpserver-ruby32        256MiB  1      silent-resonance-1jtz5c66.fra.unikraf…  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete httpserver-ruby32-s6l8n
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `server.rb`: the actual Ruby HTTP server
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

The following options are available for customizing the app:

* If you only update the implementation in the `server.rb` source file, you don't need to make any other changes.

* If you create any new source files, copy them into the app filesystem by using the `COPY` command in the `Dockerfile`.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
