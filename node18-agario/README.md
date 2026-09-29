# Agar.io (Node)

[Agar.io](https://agar.io/) is a popular multiplayer game where players control a cell and aim to grow by consuming smaller cells while avoiding being consumed by larger ones.
This guide deploys an implementation of the game using Node.js on Unikraft Cloud.

To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/node18-agario/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/node18-agario/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/node18-agario:latest
unikraft run --metro fra \
  -m 1G \
  -p 443:3000/tls+http \
  --scale-to-zero policy=on,cooldown-time=2000,stateful=true \
  --image <my-org>/node18-agario:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         node18-agario-5k2xp
uuid:         b3c4d5e6-f7a8-9b0c-1d2e-b3c4d5e6f7a8
state:        starting
image:        <my-org>/node18-agario
resources:
  memory:     1024MiB
  vcpus:      1
service:
  uuid:       c4d5e6f7-a8b9-0c1d-2e3f-c4d5e6f7a8b9
  name:       dark-meadow-fj9tm6bq
  domains:
  - fqdn:     dark-meadow-fj9tm6bq.fra.unikraft.app
networks:
- uuid:       d5e6f7a8-b9c0-1d2e-3f4a-d5e6f7a8b9c0
  private-ip: 10.0.3.5
  mac:        12:b0:b1:8d:f0:ea
timestamps:
  created:    just now
```

In this case, the instance name is `node18-agario-5k2xp` and the address is `https://dark-meadow-fj9tm6bq.fra.unikraft.app`.
They're different for each run.

The command will deploy an `agar.io` alternative called `https://github.com/owenashurst/agar.io-clone`.

After deploying, you can query the service using the provided URL.

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                 STATE    IMAGE                   ARGS  MEMORY   VCPUS  FQDN                                   CREATED
fra    node18-agario-5k2xp  running  <my-org>/node18-agario        1024MiB  1      dark-meadow-fj9tm6bq.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete <instance-name>
```

## Learn more

- [Node.js's Documentation](https://nodejs.org/docs/latest/api/)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)


Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
