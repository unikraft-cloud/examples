"""End-to-end test for the ``httpserver-python3.12-flask3.0-sqlite-distroless`` example.

Mirrors the manual steps from ``httpserver-python3.12-flask3.0-sqlite-distroless/README.md``:

1. ``unikraft build . --output <prefix>/httpserver-python312-flask30-sqlite-distroless:<tag>``
2. ``unikraft run --metro <metro> -p 443:8080/tls+http -m 768M --image ...``
3. ``curl https://<instance-url>`` and assert the FlaskBlog welcome page.
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_name, extract_instance_url


def test_httpserver_flask_sqlite_serves_page(build_image, run_instance, http, wait_instance):
    image = build_image(
        "httpserver-python3.12-flask3.0-sqlite-distroless",
        "httpserver-python3.12-flask3.0-sqlite-distroless",
    )

    instance = run_instance(
        image,
        publish=["443:8080/tls+http"],
        memory="768M",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    wait_instance(extract_instance_name(instance), "running")

    resp = http(url)
    assert resp.status_code == 200
    assert "FlaskBlog" in resp.text
