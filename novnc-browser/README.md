# Remote Desktops: noVNC

Remote desktops put a full Linux GUI behind a browser tab, which powers agentic computer-use workloads, secure browsing sessions, and disposable workstations.
They are memory-hungry and used in short, interactive bursts, so each desktop runs in its own instance that scales to zero between sessions.

This guide explains how to create and deploy a [noVNC](https://novnc.com/info.html) app, allowing you to access remote desktops through
a web interface inside a modern browser.

**Note**: Anthropic's [Computer Use Demo](https://github.com/anthropics/claude-quickstarts/tree/main/computer-use-demo) inspired this example.

To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/novnc-browser` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/novnc-browser/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/novnc-browser:latest
unikraft run --metro fra \
  -m 4G \
  -p 443:6080/tls+http \
  --scale-to-zero policy=on,cooldown-time=4000,stateful=true \
  --image <my-org>/novnc-browser:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         vnc-browser
uuid:         90a59b05-0ae1-4ca6-8383-79c5115355ee
state:        starting
image:        <my-org>/novnc-browser
resources:
  memory:     4096MiB
  vcpus:      1
service:
  uuid:       aaf03f7c-65e6-5624-d5f4-84e87450beee
  name:       weathered-fog-y5jjmwfd
  domains:
  - fqdn:     weathered-fog-y5jjmwfd.fra.unikraft.app
networks:
- uuid:       61708609-d291-572d-4a4c-399413238199
  private-ip: 10.0.0.49
  mac:        12:b0:1e:47:6c:59
timestamps:
  created:    just now
```

In this case, the instance name is `vnc-browser` and the address is `https://weathered-fog-y5jjmwfd.fra.unikraft.app`.
The name was preset, but the address is different for each run.
Enter the provided address into your browser of choice to access the remote desktop interface.

> [!WARNING]
> This exposes an unauthenticated remote desktop interface to the public internet.
> To require authentication, use websockify [authentication plugins](https://github.com/novnc/websockify/blob/v0.12.0/README.md#additional-websockify-features) (`--auth-plugin`, `--auth-source`, `--web-auth`).
> See [`auth_plugins.py`](https://github.com/novnc/websockify/blob/v0.12.0/websockify/auth_plugins.py) for the available plugins.

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME         STATE    IMAGE                   ARGS  MEMORY  VCPUS  FQDN                                     CREATED
fra    vnc-browser  standby  <my-org>/novnc-browser        4.0GiB  1      weathered-fog-y5jjmwfd.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete vnc-browser
```

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
