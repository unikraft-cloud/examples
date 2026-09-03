"""End-to-end test for the ``httpserver-java17-springboot`` example.

Mirrors the manual steps from ``httpserver-java17-springboot/README.md``:

1. ``unikraft build . --output <prefix>/httpserver-java17-springboot:<tag>``
2. ``unikraft run --metro <metro> -p 443:8080/tls+http -m 1G --image ...``
3. ``curl https://<instance-url>/hello`` and assert "Hello, World!".
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_name, extract_instance_url


def test_springboot_serves_hello(build_image, run_instance, http, wait_instance):
    image = build_image("httpserver-java17-springboot-distroless", "httpserver-java17-springboot-distroless")

    instance = run_instance(
        image,
        publish=["443:8080/tls+http"],
        memory="1G",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    wait_instance(extract_instance_name(instance), "running")

    resp = http(f"{url}/hello")
    assert resp.status_code == 200
    assert "Hello, World!" in resp.text
