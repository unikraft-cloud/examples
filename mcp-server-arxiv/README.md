# MCP Servers: ArXiv MCP Server

[MCP (Model Context Protocol)](https://modelcontextprotocol.io/docs/getting-started/intro) servers are the bridge between AI assistants and real-world resources such as file systems, databases, APIs, and search engines.
AI interactions are bursty, so a server that scales to zero when unused and wakes in milliseconds only costs you for the queries it answers.

This example demonstrates how to deploy the [ArXiv MCP server](https://github.com/blazickjp/arxiv-mcp-server) on Unikraft Cloud.

The ArXiv MCP Server is a third-party library that provides stdio-based MCP tools for accessing arXiv research papers.
This example uses [FastMCP 2.0](https://github.com/jlowin/fastmcp) to create a proxy MCP server that exposes these tools over streamable HTTP.

The server gives AI agents and assistants the ability to:

* Search for papers with filters for date ranges and categories
* Download and read paper content
* List downloaded papers
* Analyze papers using specialized prompts.

## Running on Unikraft Cloud

To run this MCP server on Unikraft Cloud:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

1. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/mcp-server-arxiv/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/mcp-server-arxiv/
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
unikraft build . --output <my-org>/mcp-server-arxiv:latest
unikraft run --metro fra \
  -m 2G \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000,stateful=true \
  --image <my-org>/mcp-server-arxiv:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy \
  -M 2Gi \
  -p 443:8080/tls+http \
  --scale-to-zero on \
  --scale-to-zero-stateful \
  --scale-to-zero-cooldown 1s \
  .
```

The output shows your instance details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         mcp-server-arxiv-l7l24
uuid:         1a721bb8-4472-4149-9870-789b1df5f80a
state:        starting
image:        <my-org>/mcp-server-arxiv
resources:
  memory:     2048MiB
  vcpus:      1
service:
  uuid:       94b10356-3df8-b2fa-cd17-60ca8193c86c
  name:       billowing-breeze-nuusy7l2
  domains:
  - fqdn:     billowing-breeze-nuusy7l2.fra.unikraft.app
networks:
- uuid:       e6754486-5398-bb06-420e-de23ed73da3f
  private-ip: 10.0.1.149
  mac:        12:b0:26:13:a0:89
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: mcp-server-arxiv-l7l24
 ├───────── uuid: 1a721bb8-4472-4149-9870-789b1df5f80a
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://billowing-breeze-nuusy7l2.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/mcp-server-arxiv@sha256:ea1e677ccc03628a3e7d57a4cd41118e3d2a631bcb2c34203bb9b175e7977f00
 ├─────── memory: 2048 MiB
 ├────── service: billowing-breeze-nuusy7l2
 ├─ private fqdn: mcp-server-arxiv-l7l24.internal
 └─── private ip: 10.0.1.149
```

In this case, the instance name is `mcp-server-arxiv-l7l24` and the service `billowing-breeze-nuusy7l2`.
They're different for each run.

For testing, you can use the example client included in this directory.
First, [install `uv`](https://docs.astral.sh/uv/getting-started/installation/) if you haven't already, then run:

```bash
export MCP_SERVER_URL=https://billowing-breeze-nuusy7l2.fra.unikraft.app/mcp
uv run client.py
```

```bash
Connecting to https://billowing-breeze-nuusy7l2.fra.unikraft.app/mcp...

--- Listing Tools ---
Name: search_papers
Description: Search for papers on arXiv with advanced filtering and query optimization.
...
```

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                    STATE    IMAGE                      ARGS  MEMORY  VCPUS  FQDN                                    CREATED
fra    mcp-server-arxiv-l7l24  standby  <my-org>/mcp-server-arxiv        2.0GiB  1      billowing-breeze-nuusy7l2.fra.unikraf…  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                    FQDN                                        STATE    STATUS   IMAGE                                                   MEMORY   VCPUS  ARGS  BOOT TIME
mcp-server-arxiv-l7l24  billowing-breeze-nuusy7l2.fra.unikraft.app  standby  standby  oci://unikraft.io/<my-org>/mcp-server-arxiv@sha256:...  2.0 GiB  1            213.07 ms
```

When done, you can delete the instance with:

```bash
kraft cloud instance remove mcp-server-arxiv-l7l24
```

## Using volumes

You can use [volumes](https://unikraft.com/docs/platform/volumes) for data persistence.
For that you would first create a volume:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft volume create --set metro=fra --set name=mcp-server-arxiv-data --set size=500M
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud volume create --name mcp-server-arxiv-data --size 500Mi
```

Then start the MCP server instance and mount that volume (while specifying the storage path):

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft build . --output <my-org>/mcp-server-arxiv:latest
unikraft run --metro fra \
  -m 2G \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000,stateful=true \
  -v mcp-server-arxiv-data:/volume \
  --image <my-org>/mcp-server-arxiv:latest \
  -- "/usr/local/bin/python /src/server.py --storage-path /volume"
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy \
  -M 2Gi \
  -p 443:8080/tls+http \
  --scale-to-zero on \
  --scale-to-zero-stateful \
  --scale-to-zero-cooldown 1s \
  -v mcp-server-arxiv-data:/volume \
  --entrypoint "/usr/local/bin/python /src/server.py --storage-path /volume" \
  .
```

## Available tools

The ArXiv MCP Server provides the following tools:

* **search_papers**: Query arXiv papers with filters for date ranges and categories
* **download_paper**: Download a paper by its arXiv ID
* **list_papers**: View all downloaded papers
* **read_paper**: Access the content of a downloaded paper

## Learn more

* [ArXiv MCP Server Documentation](https://github.com/blazickjp/arxiv-mcp-server)
* [FastMCP documentation](https://gofastmcp.com/getting-started/welcome)
* [Model Context Protocol](https://modelcontextprotocol.io/)
* [Unikraft Cloud Documentation](https://unikraft.com/docs/)
* [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)

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
