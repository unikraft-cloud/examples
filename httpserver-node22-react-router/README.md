# React Router HTTP Server

This guide shows how to deploy a [React Router](https://reactrouter.com/) app (formerly Remix).

To do so, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-node22-react-router/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-node22-react-router/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-node22-react-router:latest
unikraft run --metro fra \
  -m 768M \
  -p 443:3000/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/httpserver-node22-react-router:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         httpserver-node22-react-router-jvj6b
uuid:         4e6ccb1f-0533-4dc1-be67-eca8dfc1f8c6
state:        starting
image:        <my-org>/httpserver-node22-react-router
resources:
  memory:     768MiB
  vcpus:      1
service:
  uuid:       46865b94-fd59-7d38-485d-c110a41b0949
  name:       long-star-1tms9h1z
  domains:
  - fqdn:     long-star-1tms9h1z.fra.unikraft.app
networks:
- uuid:       270bdb2f-42a2-f26d-4a8c-43de55608490
  private-ip: 10.0.6.8
  mac:        12:b0:00:61:6e:70
timestamps:
  created:    just now
```

In this case, the instance name is `httpserver-node22-react-router-jvj6b` and the address is `https://long-star-1tms9h1z.fra.unikraft.app`.
They're different for each run.
You can now point your browser at the address to see your deployed instance.

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                           STATE    IMAGE                             ARGS  MEMORY  VCPUS  FQDN                                 CREATED
fra    httpserver-node22-react-router-jvj6b  running  <my-org>/httpserver-node22-react-router        768MiB  1      long-star-1tms9h1z.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete httpserver-node22-react-router-jvj6b
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem
* `server.js`: the server itself

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
