# Wings.io (Node)

[Wings.io](https://wings.io/) is a multiplayer .io game where players control a plane and try to shoot down other players while avoiding being shot themselves.
This guide deploys an implementation of the game using Node.js on Unikraft Cloud.

To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/node18-wingsio/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/node18-wingsio/
   ```
Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/node18-wingsio:latest
unikraft run --metro fra \
  -m 1G \
  -p 443:3000/tls+http \
  --scale-to-zero policy=on,cooldown-time=1500,stateful=true \
  --image <my-org>/node18-wingsio:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         node18-wingsio-h4n8m
uuid:         c4d5e6f7-a8b9-0c1d-2e3f-c4d5e6f7a8b9
state:        starting
image:        <my-org>/node18-wingsio
resources:
  memory:     1024MiB
  vcpus:      1
service:
  uuid:       d5e6f7a8-b9c0-1d2e-3f4a-d5e6f7a8b9c0
  name:       swift-cloud-gk7us4cz
  domains:
  - fqdn:     swift-cloud-gk7us4cz.fra.unikraft.app
networks:
- uuid:       e6f7a8b9-c0d1-2e3f-4a5b-e6f7a8b9c0d1
  private-ip: 10.0.4.4
  mac:        12:b0:c2:9e:01:fb
timestamps:
  created:    just now
```

In this case, the instance name is `node18-wingsio-h4n8m` and the address is `https://swift-cloud-gk7us4cz.fra.unikraft.app`.
They're different for each run.

The command will deploy an `wings.io` alternative called `https://github.com/Blendlight/wings.io-clone-io`.

After deploying, you can query the service using the provided URL.

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                  STATE    IMAGE                    ARGS  MEMORY   VCPUS  FQDN                                   CREATED
fra    node18-wingsio-h4n8m  running  <my-org>/node18-wingsio        1024MiB  1      swift-cloud-gk7us4cz.fra.unikraft.app  2 minutes ago
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
