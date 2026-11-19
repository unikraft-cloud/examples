"""End-to-end test for the ``httpserver-python3.12-django5.0-distroless`` example.

Mirrors the manual steps from ``httpserver-python3.12-django5.0-distroless/README.md``:

1. ``unikraft build . --output <prefix>/httpserver-python312-django50-distroless:<tag>``
2. ``unikraft run --metro <metro> -p 443:80/tls+http -m 1G --image ...``
3. ``curl https://<instance-url>/admin/`` and assert the Django admin is served.

The default Django project only defines the ``/admin/`` URL pattern, so we
test that endpoint rather than the root.
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_name, extract_instance_url


def test_django_serves_admin(build_image, run_instance, http, wait_instance):
    image = build_image("httpserver-python3.12-django5.0-distroless", "httpserver-python3.12-django5.0-distroless")

    instance = run_instance(
        image,
        publish=["443:80/tls+http"],
        memory="1G",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    wait_instance(extract_instance_name(instance), "running")

    resp = http(f"{url}/admin/", expected_status=200)
    assert resp.status_code == 200
    assert "Django" in resp.text
