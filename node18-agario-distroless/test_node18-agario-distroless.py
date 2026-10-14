"""End-to-end test for the ``node18-agario-distroless`` example.

Mirrors the manual steps from ``node18-agario-distroless/README.md``:

1. ``unikraft build . --output <prefix>/node18-agario-distroless:<tag>``
2. ``unikraft run --metro <metro> -p 443:3000/tls+http -m 1G --image ...``
3. Point browser at the instance URL and verify the game page loads.
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_name, extract_instance_url


def test_agario_serves_page(build_image, run_instance, http, wait_instance):
    image = build_image("node18-agario-distroless", "node18-agario-distroless")

    instance = run_instance(
        image,
        publish=["443:3000/tls+http"],
        memory="1G",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    wait_instance(extract_instance_name(instance), "running")

    resp = http(url)
    assert resp.status_code == 200
    assert "<html" in resp.text.lower()
