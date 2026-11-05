"""End-to-end test for the ``httpserver-java17-spring-petclinic-distroless`` example.

Mirrors the manual steps from ``httpserver-java17-spring-petclinic-distroless/README.md``:

1. ``unikraft build . --output <prefix>/httpserver-java17-spring-petclinic-distroless:<tag>``
2. ``unikraft run --metro <metro> -p 443:8080/tls+http -m 1G --image ...``
3. ``curl https://<instance-url>`` and assert the PetClinic UI is served.
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_name, extract_instance_url


def test_spring_petclinic_distroless_serves_page(build_image, run_instance, http, wait_instance):
    image = build_image("httpserver-java17-spring-petclinic-distroless", "httpserver-java17-spring-petclinic-distroless")

    instance = run_instance(
        image,
        publish=["443:8080/tls+http"],
        memory="1G",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    wait_instance(extract_instance_name(instance), "running")

    resp = http(url)
    assert resp.status_code == 200
    assert "PetClinic" in resp.text
