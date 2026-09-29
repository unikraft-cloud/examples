# Traefik

This example uses the [`Traefik`](https://traefik.io/traefik/) cloud native app proxy.
To run it, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/traefik/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/traefik/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/traefik:latest
unikraft run --metro fra \
  -m 1G \
  -p 443:80/tls+http \
  -p 8080:8080/tls \
  --scale-to-zero policy=on,cooldown-time=1000,stateful=true \
  --image <my-org>/traefik:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         traefik-wqe7e
uuid:         69d25b0b-1813-4a3f-88e6-64abbc78b359
state:        starting
image:        <my-org>/traefik
resources:
  memory:     1024MiB
  vcpus:      1
service:
  uuid:       ec7570da-5700-01b5-aaa1-0734498c11eb
  name:       holy-cherry-rye39b1x
  domains:
  - fqdn:     holy-cherry-rye39b1x.fra.unikraft.app
networks:
- uuid:       b59f4362-dc72-7efe-477b-1efe227e1b08
  private-ip: 10.0.28.16
  mac:        12:b0:31:58:d7:d0
timestamps:
  created:    just now
```

In this case, the instance name is `traefik-wqe7e` and the address is `https://holy-cherry-rye39b1x.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of Traefik.

```bash
curl https://holy-cherry-rye39b1x.fra.unikraft.app:8080/dashboard
```

```text
<!DOCTYPE html><html><head><title>Traefik</title><meta charset=utf-8><meta name=description content="Traefik UI"> ...
```

Or better yet, point a browser at the dashboard.

> **Danger:**
> This set up exposes the dashboard on port 8080 without authentication.
> Please change default.toml as needed.

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME           STATE    IMAGE             ARGS  MEMORY   VCPUS  FQDN                                   CREATED
fra    traefik-wqe7e  running  <my-org>/traefik        1024MiB  1      holy-cherry-rye39b1x.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete traefik-wqe7e
```

## Customize your app

To customize Traefik app you can change the `default.toml` configuration file.

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
