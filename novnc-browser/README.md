# Remote Desktops: noVNC

Remote desktops put a full Linux GUI behind a browser tab, which powers agentic computer-use workloads, secure browsing sessions, and disposable workstations.
They are memory-hungry and used in short, interactive bursts, so each desktop runs in its own instance that scales to zero between sessions.

This guide explains how to create and deploy a [noVNC](https://novnc.com/info.html) app, allowing you to access remote desktops through
a web interface inside a modern browser.

**Note**: Anthropic's [Computer Use Demo](https://github.com/anthropics/claude-quickstarts/tree/main/computer-use-demo) inspired this example.

To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/novnc-browser` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/novnc-browser/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft login
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
# Set Unikraft Cloud access token
export UKC_TOKEN=token
# Set metro to Frankfurt, DE
export UKC_METRO=fra
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft build . --output <my-org>/novnc-browser:latest
unikraft run --metro fra \
  -m 4G \
  -p 443:6080/tls+http \
  --scale-to-zero policy=on,cooldown-time=4000,stateful=true \
  --image <my-org>/novnc-browser:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy \
  -n vnc-browser \
  -M 4Gi \
  -p 443:6080/tls+http \
  --scale-to-zero on \
  --scale-to-zero-stateful \
  --scale-to-zero-cooldown 4s \
  .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
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

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: vnc-browser
 ├───────── uuid: 90a59b05-0ae1-4ca6-8383-79c5115355ee
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://weathered-fog-y5jjmwfd.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/novnc-browser@sha256:fdb4887e84362ebbaf54c713e0d85f547e8ee173fe63a6ab39e94b7e612a9892
 ├─────── memory: 4096 MiB
 ├────── service: weathered-fog-y5jjmwfd
 ├─ private fqdn: vnc-browser.internal
 └─── private ip: 10.0.0.49
```

In this case, the instance name is `vnc-browser` and the address is `https://weathered-fog-y5jjmwfd.fra.unikraft.app`.
The name was preset, but the address is different for each run.
Enter the provided address into your browser of choice to access the remote desktop interface.

Use `curl` to query the Unikraft Cloud instance:

```bash
curl https://weathered-fog-y5jjmwfd.fra.unikraft.app
```

```text
Hello, World!
```

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME         STATE    IMAGE                   ARGS  MEMORY  VCPUS  FQDN                                     CREATED
fra    vnc-browser  standby  <my-org>/novnc-browser        4.0GiB  1      weathered-fog-y5jjmwfd.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME         FQDN                                     STATE    STATUS   IMAGE                                                MEMORY   VCPUS  ARGS  BOOT TIME
vnc-browser  weathered-fog-y5jjmwfd.fra.unikraft.app  standby  standby  oci://unikraft.io/<my-org>/novnc-browser@sha256:...  4.0 GiB  1            7.17 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete vnc-browser
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove vnc-browser
```

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft --help
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft) or the [legacy CLI Reference](https://unikraft.com/docs/cli/kraft/overview).
