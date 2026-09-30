"""End-to-end test for the ``node21-websocket-distroless`` example.

Mirrors the manual steps from ``node21-websocket-distroless/README.md`` and the
existing CI workflow (example-node21-websocket-stable.yaml):

1. ``unikraft build . --output <prefix>/node21-websocket-distroless:<tag>``
2. ``unikraft run --metro <metro> -p 443:8080/tls+http -m 1G --image ...``
3. Connect via WebSocket (wss://) and verify echo behaviour.

The CI workflow sends "hello" and asserts it is echoed back.  We also
verify the initial greeting message and multiple echo round-trips.
"""

from __future__ import annotations

import asyncio

import websockets

from _testlib.unikraft import extract_instance_fqdn, extract_instance_name


async def _websocket_test(host: str) -> None:
    """Connect to the WebSocket server and exercise its echo behaviour."""
    uri = f"wss://{host}"

    conn = await asyncio.wait_for(
        websockets.connect(uri),
        timeout=10,
    )
    async with conn:
        # ------------------------------------------------------------------
        # 1. Greeting — server sends a welcome message on connect.
        # ------------------------------------------------------------------
        greeting = await asyncio.wait_for(conn.recv(), timeout=10)
        assert "Connection received" in greeting

        # ------------------------------------------------------------------
        # 2. Echo — matches CI workflow assertion (send "hello", expect it back).
        # ------------------------------------------------------------------
        await conn.send("hello")
        reply = await asyncio.wait_for(conn.recv(), timeout=10)
        assert reply.decode() == "hello"

        # ------------------------------------------------------------------
        # 3. Multiple echo round-trips — verify stateless echo behaviour.
        # ------------------------------------------------------------------
        messages = ["foo", "bar baz", "🚀 unicode test", ""]
        for msg in messages:
            await conn.send(msg)
            reply = await asyncio.wait_for(conn.recv(), timeout=10)
            assert reply.decode() == msg, f"expected {msg!r}, got {reply!r}"


def test_node21_websocket(build_image, run_instance, wait_instance):
    """Build, deploy, and exercise a Node.js WebSocket echo server."""
    image = build_image("node21-websocket-distroless", "node21-websocket-distroless")

    instance = run_instance(
        image,
        publish=["443:8080/tls+http"],
        memory="1G",
    )

    host = extract_instance_fqdn(instance)
    assert host, f"could not determine instance FQDN from: {instance!r}"

    wait_instance(extract_instance_name(instance), "running")
    asyncio.run(_websocket_test(host))
