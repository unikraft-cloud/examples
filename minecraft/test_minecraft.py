"""End-to-end test for the ``minecraft`` example.

Mirrors the manual steps from ``minecraft/README.md``:

1. ``unikraft build . --output <prefix>/minecraft:<tag>``
2. ``unikraft run --metro <metro> --name <tpl> -m 4096M --vcpus 4
   --image ... --rom dir=base,at=/rom/base``
   (the instance initialises and auto-converts into a template)
3. ``unikraft run --metro <metro> -p 25565:25565/tls -p 2222:2222/tls
   --template <tpl>``
4. Connect to the Minecraft port via socat and verify the server responds
   with a valid SLP (Server List Ping) status packet.
"""

from __future__ import annotations

import json
import socket
import struct
import time
import uuid

import pytest

from _testlib.unikraft import extract_instance_fqdn

MINECRAFT_PORT = 25565


def _minecraft_slp(host: str, port: int) -> dict:
    """Perform a Minecraft Server List Ping (SLP) and return the status JSON.

    Implements the modern (1.7+) SLP protocol:
    1. Send Handshake packet (id=0x00) with next-state=1 (status).
    2. Send Status Request packet (id=0x00).
    3. Read Status Response packet (id=0x00) containing JSON.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(30)
    try:
        sock.connect((host, port))

        # -- Handshake packet --
        # Protocol version (-1 = unspecified), server address, port, next state=1
        protocol_version = _encode_varint(-1 & 0xFFFFFFFF)
        server_addr = host.encode("utf-8")
        handshake_data = (
            protocol_version
            + _encode_varint(len(server_addr))
            + server_addr
            + struct.pack(">H", port)
            + _encode_varint(1)  # next state: status
        )
        _send_packet(sock, 0x00, handshake_data)

        # -- Status Request packet (empty payload) --
        _send_packet(sock, 0x00, b"")

        # -- Read Status Response --
        _length = _read_varint(sock)
        packet_id = _read_varint(sock)
        assert packet_id == 0x00, f"unexpected packet id: {packet_id}"

        json_length = _read_varint(sock)
        json_data = _recv_exact(sock, json_length)
        return json.loads(json_data.decode("utf-8"))
    finally:
        sock.close()


def _encode_varint(value: int) -> bytes:
    result = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        if value != 0:
            byte |= 0x80
        result.append(byte)
        if value == 0:
            break
    return bytes(result)


def _read_varint(sock: socket.socket) -> int:
    result = 0
    num_read = 0
    while True:
        data = _recv_exact(sock, 1)
        byte = data[0]
        result |= (byte & 0x7F) << (7 * num_read)
        num_read += 1
        if (byte & 0x80) == 0:
            break
        if num_read > 5:
            raise ValueError("VarInt too long")
    return result


def _recv_exact(sock: socket.socket, n: int) -> bytes:
    buf = bytearray()
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("connection closed while reading")
        buf.extend(chunk)
    return bytes(buf)


def _send_packet(sock: socket.socket, packet_id: int, data: bytes) -> None:
    packet_id_bytes = _encode_varint(packet_id)
    length = len(packet_id_bytes) + len(data)
    sock.sendall(_encode_varint(length) + packet_id_bytes + data)


@pytest.fixture
def _minecraft_template(request, unikraft, repo_root, ukc_image_prefix, test_run_id):
    """Build the base image and wait for the template to be ready.

    Returns the template name.
    """
    context = repo_root / "minecraft"
    base_tag = f"{ukc_image_prefix}/minecraft:{test_run_id}"
    template_name = f"minecraft-{test_run_id}"

    def _cleanup_template():
        unikraft.run(
            ["instance", "template", "delete", template_name],
            check=False,
        )

    def _cleanup_base():
        unikraft.delete_image(base_tag)

    request.addfinalizer(_cleanup_template)
    request.addfinalizer(_cleanup_base)

    # 1. Build the base image.
    unikraft.build(context, base_tag)

    # 2. Run the base image with the base ROM; it auto-converts into a template.
    unikraft.run_instance(
        base_tag,
        memory="4096M",
        name=template_name,
        vcpus=4,
        rom={"dir": context / "base", "at": "/rom/base"},
    )

    # 3. Wait for the template to be ready (Minecraft init can be slow).
    for _ in range(60):
        time.sleep(10)
        proc = unikraft.run(
            ["instance", "template", "ls"],
            check=False,
        )
        if proc.returncode == 0 and template_name in proc.stdout:
            break
    else:
        pytest.fail(f"template {template_name!r} did not become ready within timeout")

    return template_name


def test_minecraft_server_responds(
    _minecraft_template, request, unikraft, test_run_id, socat_tunnel, wait_instance
):
    """Run a Minecraft instance from template and verify SLP response."""
    template_name = _minecraft_template

    instance_name = f"mc-{test_run_id}"
    request.addfinalizer(lambda: unikraft.delete_instance(instance_name))

    instance = unikraft.run_instance(
        publish=["25565:25565/tls", "2222:2222/tls"],
        name=instance_name,
        template=template_name,
        scale_to_zero={"policy": "on", "cooldown-time": "5000", "stateful": "true"},
    )

    host = extract_instance_fqdn(instance)
    assert host, f"could not determine instance FQDN from: {instance!r}"

    # Set up a socat TLS tunnel to the Minecraft port.
    tunnel = socat_tunnel(host, MINECRAFT_PORT, MINECRAFT_PORT)

    wait_instance(instance_name, "standby")
    status = _minecraft_slp("127.0.0.1", tunnel.local_port)

    # Verify the response contains expected fields.
    assert "version" in status, f"missing 'version' in SLP response: {status}"
    assert "description" in status, f"missing 'description' in SLP response: {status}"
