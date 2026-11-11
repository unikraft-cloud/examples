"""End-to-end test for the ``httpserver-elixir1.19`` example.

Mirrors the manual steps from ``httpserver-elixir1.19/README.md``:

1. ``unikraft build . --output <prefix>/httpserver-elixir119:<tag>``
2. ``unikraft run --metro <metro> -p 443:3000/tls+http -m 1G --image ...``
3. ``curl https://<instance-url>`` and assert "Hello, World!".
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_name, extract_instance_url


def test_httpserver_elixir_serves_hello(build_image, run_instance, http, wait_instance):
    image = build_image("httpserver-elixir1.19", "httpserver-elixir1.19")

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
    assert "Hello, World!" in resp.text
