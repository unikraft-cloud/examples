"""End-to-end test for the ``memcached1.6`` example.

Mirrors the manual steps from ``memcached1.6/README.md``:

1. ``unikraft build . --output <prefix>/memcached16:<tag>``
2. ``unikraft run --metro <metro> -p 11211:11211/tls -m 256M --image ...``
3. Connect via the Memcached protocol and run set / get / incr operations.

The README demonstrates via telnet::

    set test 0 0 1
    0
    incr test 1    → 1
    incr test 1    → 2

We replicate the same set/get/incr flow using ``pymemcache``.
"""

from __future__ import annotations

import ssl

from pymemcache.client.base import Client as MemcacheClient
from pymemcache.exceptions import MemcacheError, MemcacheUnexpectedCloseError

from _testlib.readiness import retry_until_ready
from _testlib.unikraft import extract_instance_fqdn, extract_instance_name

MEMCACHED_PORT = 11211


def _connect(host: str) -> MemcacheClient:
    """Open a pymemcache client to the instance over TLS, ready to use.

    pymemcache connects lazily, so constructing the client proves nothing;
    ``version()`` is a cheap command that forces the connection, and is
    therefore what we retry while the server finishes starting.
    """
    ctx = ssl.create_default_context()

    client = MemcacheClient(
        (host, MEMCACHED_PORT),
        tls_context=ctx,
        connect_timeout=30,
        timeout=30,
    )

    retry_until_ready(
        client.version,
        exceptions=(OSError, MemcacheError),
        description="memcached",
    )

    return client


def test_memcached(build_image, run_instance, wait_instance):
    """Build, deploy, and exercise a Memcached instance."""
    image = build_image("memcached1.6", "memcached16")

    instance = run_instance(
        image,
        publish=["11211:11211/tls"],
        memory="256M",
    )

    host = extract_instance_fqdn(instance)
    assert host, f"could not determine instance FQDN from: {instance!r}"

    wait_instance(extract_instance_name(instance), "running")
    client = _connect(host)
    try:
        # ------------------------------------------------------------------
        # 1. set / get — basic key-value round-trip.
        # ------------------------------------------------------------------
        assert client.set("pytest:key", "hello")
        assert client.get("pytest:key") == b"hello"

        # ------------------------------------------------------------------
        # 2. set / incr / incr — matches the README telnet demonstration.
        #    README: set test 0 0 1 → "0", incr test 1 → 1, incr test 1 → 2
        # ------------------------------------------------------------------
        client.set("pytest:counter", "0")
        result = client.incr("pytest:counter", 1)
        assert result == 1
        result = client.incr("pytest:counter", 1)
        assert result == 2

        # ------------------------------------------------------------------
        # 3. delete — clean up and verify deletion.
        # ------------------------------------------------------------------
        assert client.delete("pytest:key")
        assert client.get("pytest:key") is None

        assert client.delete("pytest:counter")
        assert client.get("pytest:counter") is None

        # ------------------------------------------------------------------
        # 4. version — verify the server responds to the version command.
        # ------------------------------------------------------------------
        version = client.version()
        assert version is not None and len(version) > 0
    finally:
        client.close()
