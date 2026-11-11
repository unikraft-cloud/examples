"""End-to-end test for the ``httpserver-rust1.88-rocket0.5-distroless`` example.

Mirrors the manual steps from ``httpserver-rust1.88-rocket0.5-distroless/README.md``:

1. ``unikraft build . --output <prefix>/httpserver-rust188-rocket05-distroless:<tag>``
2. ``unikraft run --metro <metro> -p 443:8080/tls+http -m 256M --image ...``
3. ``curl https://<instance-url>/wave/Rocketeer/100`` and assert the greeting.
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_name, extract_instance_url


def test_httpserver_rust_rocket_serves_greeting(build_image, run_instance, http, wait_instance):
    image = build_image("httpserver-rust1.88-rocket0.5-distroless", "httpserver-rust1.88-rocket0.5-distroless")

    instance = run_instance(
        image,
        publish=["443:8080/tls+http"],
        memory="256M",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    wait_instance(extract_instance_name(instance), "running")

    resp = http(f"{url}/wave/Rocketeer/100")
    assert resp.status_code == 200
    assert "Hello" in resp.text
    assert "Rocketeer" in resp.text
