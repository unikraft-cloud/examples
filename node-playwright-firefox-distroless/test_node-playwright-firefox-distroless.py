"""End-to-end test for the ``node-playwright-firefox-distroless`` example.

Mirrors the manual steps from ``node-playwright-firefox-distroless/README.md``:

1. ``unikraft build . --output <prefix>/node-playwright-firefox-distroless:<tag>``
2. ``unikraft run --metro <metro> -p 443:8080/tls+http -m 4G --image ...``
3. ``curl https://<instance-url>/?page=https://example.com`` and assert
   the response is a valid PNG screenshot.
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_name, extract_instance_url

_PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def test_node_playwright_firefox_screenshot(build_image, run_instance, http, wait_instance):
    image = build_image(
        "node-playwright-firefox-distroless",
        "node-playwright-firefox-distroless",
    )

    instance = run_instance(
        image,
        publish=["443:8080/tls+http"],
        memory="4G",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    wait_instance(extract_instance_name(instance), "running")

    resp = http(f"{url}/?page=https://example.com")
    assert resp.status_code == 200
    assert resp.content[:8] == _PNG_MAGIC, "response is not a valid PNG image"
