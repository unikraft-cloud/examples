"""End-to-end test for the ``httpserver-node-vite-vanilla-distroless`` example.

Mirrors the manual steps from ``httpserver-node-vite-vanilla-distroless/README.md``:

1. ``unikraft build . --output <prefix>/httpserver-node-vite-vanilla-distroless:<tag>``
2. ``unikraft run --metro <metro> -p 443:8080/tls+http -m 4G --image ...``
3. ``curl https://<instance-url>`` and assert the Vite app is served.
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_name, extract_instance_url


def test_node_vite_vanilla_serves_page(build_image, run_instance, http, wait_instance):
    image = build_image("httpserver-node-vite-vanilla-distroless", "httpserver-node-vite-vanilla-distroless")

    instance = run_instance(
        image,
        publish=["443:8080/tls+http"],
        memory="4G",
        env={"PWD": "/app"},
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    wait_instance(extract_instance_name(instance), "running")

    resp = http(url)
    assert resp.status_code == 200
    assert "Vite App" in resp.text
