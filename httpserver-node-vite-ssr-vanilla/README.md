# Vite (vanilla) SSR

This example demonstrates how to run [Vite](https://vite.dev) with [server-side
rendering (SSR)](https://vite.dev/guide/ssr.html).


## Initialization

The project was instantiated via:

```
npm create vite-extra@latest node-vite-ssr-vanilla -- --template ssr-vanilla
```

The accompanying `Dockerfile` and `Kraftfile` are
necessary for deploying to Unikraft Cloud.


## Deployment

To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-node-vite-ssr-vanilla/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-node-vite-ssr-vanilla/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, run:

```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-node-vite-ssr-vanilla:latest
unikraft run --metro fra \
  -m 1G \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=2000,stateful=true \
  -e PWD=/app \
  -e NODE_ENV=production \
  --image <my-org>/httpserver-node-vite-ssr-vanilla:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         httpserver-node-vite-ssr-vanilla-k8x2m
uuid:         1a2b3c4d-5e6f-7a8b-9c0d-a1b2c3d4e5f6
state:        starting
image:        <my-org>/httpserver-node-vite-ssr-vanilla
resources:
  memory:     1024MiB
  vcpus:      1
service:
  uuid:       2b3c4d5e-6f7a-8b9c-0d1e-b2c3d4e5f6a7
  name:       warm-sky-qp3mn4rs
  domains:
  - fqdn:     warm-sky-qp3mn4rs.fra.unikraft.app
networks:
- uuid:       3c4d5e6f-7a8b-9c0d-1e2f-c3d4e5f6a7b8
  private-ip: 10.0.3.4
  mac:        12:b0:5b:2d:9a:84
timestamps:
  created:    just now
```

In this case, the instance name is `httpserver-node-vite-ssr-vanilla-k8x2m` and the address is `https://warm-sky-qp3mn4rs.fra.unikraft.app`.
They're different for each run.

After deploying, you can query the service using the provided URL.


You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                                    STATE    IMAGE                                      ARGS  MEMORY   VCPUS  FQDN                                CREATED
fra    httpserver-node-vite-ssr-vanilla-k8x2m  running  <my-org>/httpserver-node-vite-ssr-vanilla        1024MiB  1      warm-sky-qp3mn4rs.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete <instance-name>
```

## Learn more

- [NGINX's Documentation](https://nginx.org/en/docs)
- [Vite's Documentation](https://vite.dev/guide/)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs)
- [Building `Dockerfile` images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
- [Vite (vanilla) node "dev" server on Unikraft Cloud](../httpserver-node-vite-vanilla)
- [Vite (vanilla) static build on Unikraft Cloud](../httpserver-nginx-vite-vanilla)


Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
