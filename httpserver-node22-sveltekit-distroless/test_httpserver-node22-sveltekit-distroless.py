"""End-to-end test for the ``httpserver-node22-sveltekit-distroless`` example.

Mirrors the manual steps from ``httpserver-node22-sveltekit-distroless/README.md``:

1. ``unikraft build . --output <prefix>/httpserver-node22-sveltekit-distroless:<tag>``
2. ``unikraft run --metro <metro> -p 443:3000/tls+http -m 512M --image ...``
3. ``curl https://<instance-url>`` and assert the SvelteKit app is served.
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_name, extract_instance_url


def test_httpserver_sveltekit_serves_page(build_image, run_instance, http, wait_instance):
    image = build_image(
        "httpserver-node22-sveltekit-distroless",
        "httpserver-node22-sveltekit-distroless",
    )

    instance = run_instance(
        image,
        publish=["443:3000/tls+http"],
        memory="512M",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    wait_instance(extract_instance_name(instance), "running")

    resp = http(url)
    assert resp.status_code == 200
