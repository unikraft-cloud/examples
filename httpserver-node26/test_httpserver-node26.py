"""End-to-end test for the ``httpserver-node26`` example.

Mirrors the manual steps from ``httpserver-node26/README.md``:

1. ``unikraft build . --output <prefix>/httpserver-node26:<tag>``
2. ``unikraft run --metro <metro> -p 443:8080/tls+http -m 512M --image ...``
3. ``curl https://<instance-url>`` and assert "Hello, World!".
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_url


def test_httpserver_node_serves_hello(build_image, run_instance, http):
    image = build_image("httpserver-node26", "httpserver-node26")

    instance = run_instance(
        image,
        publish=["443:8080/tls+http"],
        memory="512M",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    resp = http(url)
    assert resp.status_code == 200
    assert "Hello, World!" in resp.text
