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
  -e NOVNC_PASSWORD=<my-password> \
  --scale-to-zero policy=on,cooldown-time=4000,stateful=true \
  --image <my-org>/novnc-browser:latest
```

Replace `<my-password>` with a long random password.
For more information, see [Authentication](#authentication).

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         vnc-browser
uuid:         90a59b05-0ae1-4ca6-8383-79c5115355ee
state:        starting
image:        <my-org>/novnc-browser
runtime:
  env:
    NOVNC_PASSWORD: *
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
The browser asks for a user name and a password.
Use the user name `novnc` and the password from `NOVNC_PASSWORD`.

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

## Authentication

The remote desktop uses HTTP Basic Auth when you set the `NOVNC_PASSWORD` environment variable.
Basic Auth protects the noVNC page and the WebSocket connection to the desktop.
Unikraft Cloud encrypts the connection with TLS.

| Variable         | Value                                           | Default           |
| ---------------- | ----------------------------------------------- | ----------------- |
| `NOVNC_PASSWORD` | Password for HTTP Basic Auth                    | No authentication |
| `NOVNC_USER`     | User name for HTTP Basic Auth, without a `:`    | `novnc`           |

> [!WARNING]
> If you do not set `NOVNC_PASSWORD`, the remote desktop has no authentication.
> A person who knows the address can control the desktop.
> The instance log then shows `WARNING: noVNC has no authentication`.

A program, for example an AI agent, can also use the desktop.
It must send the `Authorization: Basic <base64 of user:password>` header with each request, also with the WebSocket request to `/websockify`.
For example:

```bash
curl -u 'novnc:<my-password>' https://weathered-fog-y5jjmwfd.fra.unikraft.app/vnc.html
```

With Playwright, set the credentials on the browser context:

```python
context = browser.new_context(
    http_credentials={"username": "novnc", "password": "<my-password>"})
```

Do not put the credentials in the address (`https://user:password@...`).
Some browsers do not send them with the WebSocket request.

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
