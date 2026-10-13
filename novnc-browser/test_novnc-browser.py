"""End-to-end test for the ``novnc-browser`` example.

Mirrors the manual steps from ``novnc-browser/README.md``:

1. ``unikraft build . --output <prefix>/novnc-browser:<tag>``
2. ``unikraft run --metro <metro> -p 443:6080/tls+http -m 4G --image ...``
3. Point browser at the instance URL and verify the noVNC page loads.
"""

from __future__ import annotations

import pytest

from _testlib.unikraft import extract_instance_name, extract_instance_url


@pytest.mark.timeout(900)
def test_novnc_serves_page(build_image, run_instance, http, wait_instance):
    image = build_image("novnc-browser", "novnc-browser")

    instance = run_instance(
        image,
        publish=["443:6080/tls+http"],
        memory="4G",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    wait_instance(extract_instance_name(instance), "running")

    # noVNC starts after Xvfb, openbox, lxpanel and x11vnc, so allow some
    # time for the HTTP endpoint to become ready.
    resp = http(url, retries=30, backoff=5.0, timeout=30.0)
    assert resp.status_code == 200
    assert "noVNC" in resp.text or "vnc" in resp.text.lower()
