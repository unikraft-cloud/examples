# Visual Studio Code server

[Visual Studio Code](https://code.visualstudio.com/) is a source-code editor developed by Microsoft. It includes support for debugging, syntax highlighting, intelligent code completion, snippets, code refactoring, and embedded Git.
It features a [Code server](https://code.visualstudio.com/docs/remote/vscode-server), which allows you to run Visual Studio Code remotely and access it through a web browser or your local Visual Studio Code client.

This guide explains how to create and deploy a Visual Studio Code server app.
To run this example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/code-server` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/code-server/
```

Make sure to log into Unikraft Cloud by setting your token and a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash
export UKC_TOKEN=token
# Set metro to Frankfurt, DE
export UKC_METRO=fra
```

When done, invoke the following commands to deploy the app on Unikraft Cloud (make sure to change the `PASSWORD` and `SUDO_PASSWORD`):

```bash
kraft cloud volume create \
    --name code-workspace \
    --size 1Gi

kraft cloud deploy \
    --scale-to-zero on \
    --scale-to-zero-stateful \
    --scale-to-zero-cooldown 4s \
    -M 2048 \
    --name code-server \
    -p 443:8443 \
    -v code-workspace:/workspace \
    -e PGUID=0 \
    -e PGID=0 \
    -e PASSWORD=unikraft \
    -e SUDO_PASSWORD=unikraft \
    -e DEFAULT_WORKSPACE="/workspace" \
    .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├─────── name: code-server
 ├─────── uuid: c1a619a0-e222-4042-94b8-ba4b39353417
 ├────── metro: https://api.fra.unikraft.cloud/v1
 ├────── state: starting
 ├───── domain: https://blue-shape-chmxf1g4.fra.unikraft.app
 ├────── image: code-server@sha256:633ec8a8dcb342b093c6f055f84fc056ee1abe40ff56e98bd612c4b9d4ddffcb 
 ├───── memory: 2048 MiB
 ├──── service: blue-shape-chmxf1g4
 ├─ private ip: 10.0.0.49
 └─────── args: /app/code-server/bin/code-server --host 0.0.0.0 --port 8443 --auth password
```

This will create a volume for data persistence, and mount it at `/workspace` inside the VM.

In this case, the instance name is `code-server` and the address is `https://blue-shape-chmxf1g4.fra.unikraft.app`.
The name was preset, but the address is different for each run. Enter the provided URL into your browser of choice to access the Code server instance.

You can list information about the volume by running:

```bash
kraft cloud volume list
```

```text
NAME            CREATED AT      SIZE     ATTACHED TO  MOUNTED BY   STATE      PERSISTENT
code-workspace  13 minutes ago  1.0 GiB  code-server  code-server  mounted    true
```

You can list information about the instance by running:

```bash
kraft cloud instance list
```

```ansi
NAME         FQDN                                  STATE    STATUS   IMAGE                          MEMORY   VCPUS  ARGS                                 BOOT TIME
code-server  blue-shape-chmxf1g4.fra.unikraft.app  standby  standby  code-server@sha256:633ec8a...  2.0 GiB  1      /app/code-server/bin/code-server...  8.45 ms
```

When done, you can remove the instance:

```bash
kraft cloud instance remove code-server
```

The volume is not removed by default, so you can recreate the instance and still have access to your old data. Remove it using:

```bash
kraft cloud volume remove code-workspace
```

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
