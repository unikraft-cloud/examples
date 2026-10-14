"""Simple MCP Server Python Client
-------------------------------

This script demonstrates how to connect to the Simple MCP server deployed on Unikraft Cloud using Streamable HTTP transport.
It lists available tools and tests each one.

Usage:
    export MCP_SERVER_URL=https://your-server-url/mcp
    uv run client.py
"""
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "fastmcp",
# ]
# ///

import asyncio
import os
from fastmcp import Client


async def main():
    url = os.getenv("MCP_SERVER_URL", None)
    if url is None:
        print("Error: MCP_SERVER_URL environment variable is not set.")
        print("Please set it to the server's MCP endpoint URL (e.g., https://your-server-url/mcp).")
        return

    print(f"Connecting to {url}...")

    try:
        async with Client(url) as client:
            # List available tools
            print("\n--- Listing Tools ---")
            tools = await client.list_tools()
            for tool in tools:
                print(f"Name: {tool.name}")
                print(f"Description: {tool.description}")
                print()

            # Test weather tool
            print("\n--- Testing Weather Tool ---")
            try:
                result = await client.call_tool(
                    "get_weather",
                    arguments={"city": "London"}
                )
                for content in result.content:
                    if content.type == "text":
                        print(content.text)

            except Exception as e:
                print(f"Error calling weather tool: {e}")

            # Test time tool
            print("\n--- Testing Time Tool ---")
            try:
                result = await client.call_tool(
                    "get_time",
                    arguments={"timezone": "America/New_York"}
                )
                for content in result.content:
                    if content.type == "text":
                        print(content.text)

            except Exception as e:
                print(f"Error calling time tool: {e}")

            # Test calculate tool
            print("\n--- Testing Calculate Tool ---")
            try:
                result = await client.call_tool(
                    "calculate",
                    arguments={"operation": "add", "a": 10, "b": 5}
                )
                for content in result.content:
                    if content.type == "text":
                        print(content.text)

            except Exception as e:
                print(f"Error calling calculate tool: {e}")

    except Exception as e:
        print(f"Connection error: {e}")
        print("Make sure the URL is correct and the server is running.")


if __name__ == "__main__":
    asyncio.run(main())
