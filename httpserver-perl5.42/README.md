# Perl HTTP Server

This guide explains how to create and deploy a simple Perl-based HTTP web server.
To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-perl5.42/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-perl5.42/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-perl542:latest
unikraft run --metro fra \
  -m 512M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/httpserver-perl542:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         httpserver-perl542-xue8j
uuid:         59d08bbc-cbb7-4c6b-a2cb-847828845db9
state:        starting
image:        <my-org>/httpserver-perl542
resources:
  memory:     512MiB
  vcpus:      1
service:
  uuid:       b62c0c0a-2de6-9068-1e93-223fa8f1edbf
  name:       fragrant-water-wau08gaw
  domains:
  - fqdn:     fragrant-water-wau08gaw.fra.unikraft.app
networks:
- uuid:       22bdfc9c-2f69-eb7e-5b5e-929aba51a2c0
  private-ip: 10.0.1.161
  mac:        12:b0:d4:aa:c1:98
timestamps:
  created:    just now
```

In this case, the instance name is `httpserver-perl542-xue8j` and the address is `https://fragrant-water-wau08gaw.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Perl-based HTTP web server:

```bash
curl https://fragrant-water-wau08gaw.fra.unikraft.app
```

```text
Hello, World!
```

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                      STATE    IMAGE                        ARGS  MEMORY  VCPUS  FQDN                                      CREATED
fra    httpserver-perl542-xue8j  standby  <my-org>/httpserver-perl542        512MiB  1      fragrant-water-wau08gaw.fra.unikraft.app  2 minutes ago
```

When you list your instances, you might notice they show as standby.
This is normal behavior and means the instance is using Unikraft Cloud's scale-to-zero feature that saves resources when there is no traffic.
To check your instance is working, open two terminals and use these commands to watch the status:

```bash title="unikraft"
unikraft instance list --watch
# In another terminal, make requests
curl https://fragrant-water-wau08gaw.fra.unikraft.app
```

It switches to "running" then back to "standby."

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete httpserver-perl542-xue8j
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `server.pl`: the actual Perl HTTP server implementation
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

The following options are available for customizing the app:

* If you only update the implementation in the `server.pl` source file, you don't need to make any other changes.

* If you create any new source files, copy them into the app filesystem by using the `COPY` command in the `Dockerfile`.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
