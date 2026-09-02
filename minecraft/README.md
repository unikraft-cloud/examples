# Game Servers: Minecraft

Game servers have expensive startup paths, loading assets and initializing world state, and long idle stretches between sessions, which usually means paying for a server that runs all day.
Minecraft is a strong example of the pattern: JVM warm-up and world initialization happen once into a template snapshot, and an instance pauses when the last player disconnects, then resumes from that snapshot on the next connection.

This example runs a Minecraft Java server on Unikraft Cloud with:

- A reusable base image (`minecraft:latest`) built from [itzg/minecraft-server](https://hub.docker.com/r/itzg/minecraft-server) (Java 25)
- Configuration overrides through auxiliary ROMs (optional)
- Template-based startup for faster instance creation
- TLS-exposed Minecraft and SSH endpoints

## Prerequisites

1. Install the [unikraft CLI](https://unikraft.com/docs/cli/unikraft).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/minecraft/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/minecraft/
   ```

3. Review and adjust the base server settings in [`base/.env`](./base/.env).
   You can check out [this documentation](https://docker-minecraft-server.readthedocs.io/en/latest/) for available configuration options.
   Make sure to also set your `PUBKEY` for SSH access, and optionally set `TEMPLATE_WITH_WORLD` if you want the template to include the world (see below).
   Optionally, create per-config overrides in `<config>/.env` (for example [`bingo/.env`](./bingo/.env)).
   All the `.env` files are packaged as [auxiliary ROMs](https://unikraft.com/docs/features/roms) and mounted at `/rom/<config>`.

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

## Deployment Workflow

### Package the base image

First, package and push the base Minecraft server image:

```bash title="unikraft"
unikraft build . --output <my-org>/minecraft:latest
```

The image is built from the Docker image [itzg/minecraft-server](https://hub.docker.com/r/itzg/minecraft-server) and includes a few tweaks:

- The entrypoint is wrapped around a custom [`wrapper.sh`](./wrapper.sh) script that:
  - Starts an SSH server
  - Loads the environment configuration from the attached ROM(s)
  - Disables scale-to-zero before executing the original entrypoint
- The server configuration scripts from the original image are patched (see [patches/](./patches)) to trigger the template snapshot before the full warm-up of the server, which allows faster instance creation from the template.
  Scale-to-zero is enabled after server initialization.

### Create an instance template from the base image

This step is required to enable fast startups from the base image, which is particularly important for a Minecraft server given the long initialization time.
If you only customized the server using the base [`.env`](./base/.env) file, create the instance with one ROM:

```bash title="unikraft"
unikraft run --metro fra \
  --name minecraft-tpl \
  -m 4096M \
  --vcpus 4 \
  --rom dir=base,at=/rom/base \
  --image <my-org>/minecraft:latest
```

The output shows the instance details:

```ansi title="unikraft"
metro:        fra
name:         minecraft-tpl
uuid:         d9d7be54-5495-45d0-b5af-48be7f30d1d8
state:        starting
image:        <my-org>/minecraft
resources:
  memory:     4GiB
  vcpus:      4
roms:
- name:       rom
  image:      c99125f6-6b8c-4f94-b94c-e2d9551b253b
  at:         /rom
networks:
- uuid:       123b0ed0-9f2f-417c-9307-34424d80e4cb
  private-ip: 10.0.0.29
  mac:        12:b0:0a:00:00:1d
timestamps:
  created:    just now
```

If you also have per-config overrides (for example in [`bingo/.env`](./bingo/.env)), create the instance with multiple ROMs:

```bash title="unikraft"
unikraft run --metro fra \
  --name minecraft-tpl \
  -m 4096M \
  --vcpus 4 \
  --rom dir=base,at=/rom/base \
  --rom dir=bingo,at=/rom/bingo \
  --image <my-org>/minecraft:latest
```

The instance will run until initialization is complete, then it will be snapshotted as a template and immediately deleted.
The exact moment of snapshotting can be configured in [`patches/start-finalExec`](./patches/start-finalExec), but it can also be configured by the following environment variable:

- If `TEMPLATE_WITH_WORLD=true`, then the snapshot will be triggered **after** world generation
- Otherwise, the snapshot will be triggered **after** extracting the jar files and writing configuration files, **before** world generation

You can follow the logs of the instance to check the progress:

```bash title="unikraft"
unikraft instances logs minecraft-tpl -f
```

Once they stop, the template is ready and you can check it with:

```bash title="unikraft"
unikraft instances templates list
```

```bash title="unikraft"
METRO  NAME           STATE     IMAGE               ARGS  MEMORY  VCPUS  CREATED
fra    minecraft-tpl  template  <my-org>/minecraft        4GiB    4      5 seconds ago
```

### Create an instance from the template

You can now create new instances from the template, which will boot much faster than the original base image:

```bash title="unikraft"
unikraft run --metro fra \
  --name minecraft \
  -p 2222:2222/tls \
  -p 25565:25565/tls \
  --scale-to-zero policy=on,cooldown-time=5000,stateful=true \
  --template minecraft-tpl
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:         fra
name:          minecraft
uuid:          56787b5d-14fb-4908-88d0-e9609d1ac1e0
state:         running
image:         <my-org>/minecraft
resources:
  memory:      4GiB
  vcpus:       4
service:       hidden-water-ewr8l9sp
roms:
- name:        rom
  image:       c99125f6-6b8c-4f94-b94c-e2d9551b253b
  at:          /rom
networks:
- uuid:        b6c7d615-7e74-49d6-a8b6-14c39323233b
  private-ip:  10.0.0.29
  mac:         12:b0:0a:00:00:1d
timestamps:
  created:     just now
scale-to-zero: policy=on,stateful=true,cooldown-time=5s
```

In this case, the instance name is `minecraft` and the address is `https://hidden-water-ewr8l9sp.fra.unikraft.app`.

A sample log output of the server getting ready:

```bash title="unikraft"
unikraft instances logs minecraft -f
```

```text
[12:59:45] [Server thread/INFO]: Preparing spawn area: 100%
[12:59:45] [Server thread/INFO]: Time elapsed: 3641 ms
[12:59:45] [Server thread/INFO]: Done (3.850s)! For help, type "help"
[12:59:45] [Server thread/INFO]: Starting remote control listener
[12:59:45] [Server thread/INFO]: Thread RCON Listener started
[12:59:45] [Server thread/INFO]: RCON running on 0.0.0.0:25575
[12:59:45] [Server thread/INFO]: Saving chunks for level 'ServerLevel[world]'/minecraft:overworld
[12:59:45] [Server thread/INFO]: Saving chunks for level 'ServerLevel[world]'/minecraft:the_end
[12:59:45] [Server thread/INFO]: Saving chunks for level 'ServerLevel[world]'/minecraft:the_nether
[12:59:45] [Server thread/INFO]: ThreadedAnvilChunkStorage (world): All chunks are saved
[12:59:45] [Server thread/INFO]: ThreadedAnvilChunkStorage (DIM1): All chunks are saved
[12:59:45] [Server thread/INFO]: ThreadedAnvilChunkStorage (DIM-1): All chunks are saved
[12:59:45] [Server thread/INFO]: ThreadedAnvilChunkStorage: All dimensions are saved
```

## Connect to Minecraft and SSH

At the moment, Unikraft Cloud can only expose these services over TLS.
Since Minecraft clients and SSH clients do not support TLS, you can use `socat` to terminate TLS locally and expose plain TCP endpoints for your clients to connect to.

### Minecraft proxy

```bash
socat TCP-LISTEN:25565,reuseaddr,fork OPENSSL:hidden-water-ewr8l9sp.fra.unikraft.app:25565,verify=0
```

Then connect your Minecraft client to `localhost:25565`.

### SSH proxy

```bash
socat TCP-LISTEN:2222,reuseaddr,fork OPENSSL:hidden-water-ewr8l9sp.fra.unikraft.app:2222,verify=0
```

Then connect your SSH client to `localhost:2222` with the username `root` and the SSH key you configured in the `.env` file.

## Administration

### RCON

SSH into the instance (via the local TLS proxy), then run:

```bash
rcon-cli --host 127.0.0.1
```

You can then execute any Minecraft server command through the RCON interface, for example:

```bash
say Hello from Unikraft Cloud!
```

You can also give yourself operator permissions to execute these commands in-game:

```bash
/op <username>
```

### Whitelist in offline mode

Offline mode does not produce online UUIDs.
If you whitelist players manually, compute UUIDs per username and update `/data/whitelist.json`.

```python
import hashlib, uuid; h = hashlib.md5(b'OfflinePlayer:<username>').digest(); u = uuid.UUID(bytes=h); print(u)
```

Format:

```json
[
    {
        "uuid": "<uuid>",
        "name": "<username>"
    }
]
```

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
