"""End-to-end test for the ``redis7.2`` example.

Mirrors the manual steps from ``redis7.2/README.md``:

1. ``unikraft build . --output <prefix>/redis72:<tag>``
2. ``unikraft run --metro <metro> -p 6379:6379/tls -m 512M --image ...``
3. Connect with a Redis client and run PING, SET, GET, INCR, DEL.

The README demonstrates ``redis-benchmark -t ping,set,get``.
We replicate the same operations (PING, SET, GET) plus INCR and DEL.
"""

from __future__ import annotations

import redis

from _testlib.readiness import retry_until_ready
from _testlib.unikraft import extract_instance_fqdn, extract_instance_name

REDIS_PORT = 6379


def _connect(host: str) -> redis.Redis:
    """Open a redis-py client to the instance over TLS, ready to use.

    redis-py connects lazily, so constructing the client proves nothing; PING
    is the first call that actually touches the network, and is therefore what
    we retry while the server finishes starting.
    """
    client = redis.Redis(
        host=host,
        port=REDIS_PORT,
        ssl=True,
        socket_connect_timeout=30,
        decode_responses=True,
    )

    retry_until_ready(
        client.ping,
        exceptions=(redis.ConnectionError, redis.TimeoutError),
        description="redis",
    )

    return client


def test_redis(build_image, run_instance, wait_instance):
    """Build, deploy, and exercise a Redis instance."""
    image = build_image("redis7.2", "redis72")

    instance = run_instance(
        image,
        publish=["6379:6379/tls"],
        memory="512M",
    )

    host = extract_instance_fqdn(instance)
    assert host, f"could not determine instance FQDN from: {instance!r}"

    wait_instance(extract_instance_name(instance), "running")
    r = _connect(host)
    try:
        # ------------------------------------------------------------------
        # 1. PING — baseline connectivity.
        # ------------------------------------------------------------------
        r.ping()

        # ------------------------------------------------------------------
        # 2. SET / GET — key-value round-trip.
        # ------------------------------------------------------------------
        assert r.set("pytest:key", "hello") is True
        assert r.get("pytest:key") == "hello"

        # ------------------------------------------------------------------
        # 3. INCR — atomic increment (matches README benchmark operations).
        # ------------------------------------------------------------------
        r.set("pytest:counter", "0")
        r.incr("pytest:counter")
        r.incr("pytest:counter")
        assert r.get("pytest:counter") == "2"

        # ------------------------------------------------------------------
        # 4. DEL — clean up and verify deletion.
        # ------------------------------------------------------------------
        r.delete("pytest:key", "pytest:counter")
        assert r.get("pytest:key") is None
        assert r.get("pytest:counter") is None

        # ------------------------------------------------------------------
        # 5. INFO — verify server identifies as Redis.
        # ------------------------------------------------------------------
        info = r.info("server")
        assert "redis_version" in info
    finally:
        r.close()
