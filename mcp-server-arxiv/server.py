"""ArXiv MCP Server with Streamable HTTP transport.

This uses the arxiv_mcp_server library and runs it via stdio.
The server is exposed over Streamable HTTP using FastMCP's proxying capabilities.
"""


import argparse
import uvicorn
from fastmcp import FastMCP
from fastmcp.client.transports import StdioTransport
from fastmcp.server.proxy import ProxyClient


def build_mcp_proxy(storage_path):
    transport = StdioTransport(
        command="/root/.local/bin/arxiv-mcp-server",
        args=[
            "--storage-path", storage_path
        ]
    )
    return FastMCP.as_proxy(ProxyClient(transport), name="ArXivProxy")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--storage-path", type=str, default="/tmp/arxiv-papers",
                        help="Path to paper storage directory")
    args = parser.parse_args()

    mcp = build_mcp_proxy(args.storage_path)
    app = mcp.http_app(stateless_http=True)
    uvicorn.run(app, host="0.0.0.0", port=8080)
