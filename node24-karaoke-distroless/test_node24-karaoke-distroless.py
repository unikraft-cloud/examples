"""End-to-end test for the ``node24-karaoke-distroless`` example.

Mirrors the manual steps from ``node24-karaoke-distroless/README.md``:

1. ``unikraft build . --output <prefix>/node24-karaoke-distroless:<tag>``
2. ``unikraft run --metro <metro> -p 443:8080/tls+http -m 2G --image ...``
3. ``curl https://<instance-url>`` and assert the karaoke app is served.
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_name, extract_instance_url


def test_karaoke_serves_page(build_image, run_instance, http, wait_instance):
    image = build_image("node24-karaoke-distroless", "node24-karaoke-distroless")

    instance = run_instance(
        image,
        publish=["443:8080/tls+http"],
        memory="2G",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    wait_instance(extract_instance_name(instance), "running")

    resp = http(url)
    assert resp.status_code == 200
