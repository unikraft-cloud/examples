# Simple MCP Server

This example demonstrates how to build a minimal custom MCP (Model Context Protocol) server from scratch using [FastMCP 2.0](https://github.com/jlowin/fastmcp).

This is a great starting point for building your own custom MCP servers with business-specific tools and logic.

## Running on Unikraft Cloud

To run this MCP server on Unikraft Cloud:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

1. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/mcp-server-simple/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/mcp-server-simple/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/mcp-server-simple:latest
unikraft run --metro fra \
  -m 512M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000,stateful=true \
  --image <my-org>/mcp-server-simple:latest
```

The output shows your instance details:

```ansi title="unikraft"
metro:        fra
name:         mcp-server-simple-bbdcb
uuid:         e87d3591-3497-4f30-bd76-1dc886059647
state:        starting
image:        <my-org>/mcp-server-simple
resources:
  memory:     512MiB
  vcpus:      1
service:
  uuid:       3cfc78af-748d-c6ba-5bfb-427b3bd7e9aa
  name:       cool-paper-b6mht7jv
  domains:
  - fqdn:     cool-paper-b6mht7jv.fra.unikraft.app
networks:
- uuid:       6a712117-5b67-d89a-7e2e-4a57e1732724
  private-ip: 10.0.0.193
  mac:        12:b0:39:2b:a3:15
timestamps:
  created:    just now
```

In this case, the instance name is `mcp-server-simple-bbdcb` and the service `cool-paper-b6mht7jv`.
They're different for each run.

For testing, you can use the example client included in this directory.
First, [install `uv`](https://docs.astral.sh/uv/getting-started/installation) if you haven't already, then run:

```bash
export MCP_SERVER_URL=https://cool-paper-b6mht7jv.fra.unikraft.app/mcp
uv run client.py
```

```bash
Connecting to https://cool-paper-b6mht7jv.fra.unikraft.app/mcp...

--- Listing Tools ---
Name: get_weather
Description: Get current weather for a city.

Args:
    city: Name of the city

Returns:
    Weather information including temperature, conditions, and humidity

Name: get_time
Description: Get current time in a timezone.
...
```

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                     STATE    IMAGE                       ARGS  MEMORY  VCPUS  FQDN                                  CREATED
fra    mcp-server-simple-bbdcb  standby  <my-org>/mcp-server-simple        512MiB  1      cool-paper-b6mht7jv.fra.unikraft.app  2 minutes ago
```

When done, you can delete the instance with:

```bash title="unikraft"
unikraft instances delete mcp-server-simple-bbdcb
```

## Available tools

This MCP Server provides the following tools:

* **get_weather**: Get simulated weather for a city
* **get_time**: Get current time in a timezone
* **calculate**: Perform basic arithmetic operations (add, subtract, multiply, divide)

## Building your own tools

This example shows the basic structure of an MCP server using FastMCP.
To add your own tools:

1. **Define the tool** using the `@mcp.tool()` decorator:
   * Add type hints for parameters
   * Include a docstring describing what the tool does
   * Parameters are automatically converted to JSON schema

1. **Write the tool** function:
   * Process the parameters
   * Return a string result (or raise an exception for errors)

1. **Test locally** before deploying:

   ```bash
   pip install -r requirements.txt
   python server.py
   ```

Example:

```python
from fastmcp import FastMCP

mcp = FastMCP("My Custom Server")

@mcp.tool()
def my_custom_tool(param1: str, param2: int) -> str:
    """Description of what this tool does.

    Args:
        param1: Description of first parameter
        param2: Description of second parameter

    Returns:
        Result description
    """
    # Your implementation here
    return f"Processed {param1} with {param2}"

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8080)
```

## Architecture

The server uses FastMCP, a high-level framework for building MCP servers that features:

* **HTTP Transport**: Built-in Streamable HTTP transport
* **Type-Safe**: Automatic JSON schema generation from Python type hints
* **Simple API**: Decorator-based tool definitions

This provides:

* Standard MCP protocol support
* Automatic tool schema generation
* Built-in HTTP server
* Easy deployment to any platform

## Learn more

* [MCP Documentation](https://modelcontextprotocol.io/)
* [FastMCP documentation](https://gofastmcp.com/getting-started/welcome)
* [Building MCP Servers](https://modelcontextprotocol.io/docs/building-servers)
* [Unikraft Cloud Documentation](https://unikraft.com/docs/)
* [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
