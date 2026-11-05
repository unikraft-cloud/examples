"""End-to-end test for the ``httpserver-prisma-expressjs4.19-node18-distroless`` example.

Mirrors the manual steps from ``httpserver-prisma-expressjs4.19-node18-distroless/README.md``:

1. ``unikraft build . --output <prefix>/httpserver-prisma-expressjs419-node18-distroless:<tag>``
2. ``unikraft run --metro <metro> -p 443:3000/tls+http -m 512M --image ...``
3. ``curl https://<instance-url>/users`` and assert the seeded user list.
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_name, extract_instance_url


def test_httpserver_prisma_serves_users(build_image, run_instance, http, wait_instance):
    image = build_image(
        "httpserver-prisma-expressjs4.19-node18-distroless",
        "httpserver-prisma-expressjs4.19-node18-distroless",
    )

    instance = run_instance(
        image,
        publish=["443:3000/tls+http"],
        memory="512M",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    wait_instance(extract_instance_name(instance), "running")

    resp = http(f"{url}/users")
    assert resp.status_code == 200
    users = resp.json()
    assert isinstance(users, list)
    assert len(users) > 0
    assert "alice@prisma.io" in resp.text
