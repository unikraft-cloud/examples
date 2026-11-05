"""End-to-end test for the ``chromium-cdp-auth`` example.

Mirrors the manual steps from ``chromium-cdp-auth/README.md``:

1. Create a volume for the token database (mounted at ``/app/data``).
2. ``unikraft build . --output <prefix>/chromium-cdp-auth:<tag>``
3. ``unikraft run --metro <metro> --scale-to-zero policy=idle,... -m 4G
   -p 443:8080/tls+http -e BOOTSTRAP_ADMIN_TOKEN=... --volume ...:/app/data``
4. Exercise the endpoints documented in the README:

   * ``GET /health`` is public (no auth required).
   * CDP endpoints (e.g. ``/json/version``) require a valid token, passed
     either as an ``Authorization: Bearer`` header or a ``?token=`` query
     parameter.
   * The admin-only token-management API can create, list, and revoke
     tokens; revoked tokens no longer grant access.
"""

from __future__ import annotations

import logging

import requests

from _testlib.http_client import allow_insecure
from _testlib.unikraft import extract_instance_name, extract_instance_url

log = logging.getLogger(__name__)

BOOTSTRAP_ADMIN_TOKEN = "examples-pytest-admin-token"


def test_chromium_cdp_auth(build_image, run_instance, http, http_post, unikraft, request, test_run_id, wait_instance):
    volume = f"chromium-cdp-auth-data-{test_run_id}"

    def _cleanup_volume():
        try:
            unikraft.run(["volume", "delete", volume], check=False)
            log.info("deleted volume %s", volume)
        except Exception:
            log.exception("error deleting volume %s", volume)

    request.addfinalizer(_cleanup_volume)

    # 1. Create the volume backing the token database.
    unikraft.run([
        "volume", "create",
        "--metro", unikraft.metro,
        f"--name={volume}",
        "--size=64M",
    ])

    # 2. Build and deploy, passing the bootstrap admin token and mounting
    #    the volume at /app/data.
    image = build_image("chromium-cdp-auth", "chromium-cdp-auth")

    instance = run_instance(
        image,
        publish=["443:8080/tls+http"],
        memory="4G",
        scale_to_zero={"policy": "idle", "cooldown-time": "1000", "stateful": "true"},
        env={"BOOTSTRAP_ADMIN_TOKEN": BOOTSTRAP_ADMIN_TOKEN},
        volume=f"{volume}:/app/data",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    wait_instance(extract_instance_name(instance), "standby")

    admin_headers = {"Authorization": f"Bearer {BOOTSTRAP_ADMIN_TOKEN}"}

    # 3. /health is public — reachable without a token.
    resp = http(f"{url}/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

    # 4. CDP endpoints reject requests without a token.
    resp = http(f"{url}/json/version", expected_status=401)
    assert resp.status_code == 401

    # 5. The bootstrap admin token grants access, both via the
    #    Authorization header ...
    resp = http(f"{url}/json/version", headers=admin_headers)
    assert resp.status_code == 200
    assert "Browser" in resp.text

    # ... and via the ?token= query parameter.
    resp = http(f"{url}/json/version?token={BOOTSTRAP_ADMIN_TOKEN}")
    assert resp.status_code == 200
    assert "Browser" in resp.text

    # 6. The token-management API rejects unauthenticated requests.
    resp = http(f"{url}/api/tokens", expected_status=401)
    assert resp.status_code == 401

    # 7. Create a (non-admin) client token via the admin API ...
    resp = http_post(
        f"{url}/api/tokens",
        headers=admin_headers,
        json={"name": "my-client", "expiresInDays": 7},
        expected_status=201,
    )
    created = resp.json()
    client_token = created["token"]
    assert client_token, f"no token in create response: {created!r}"
    assert created["name"] == "my-client"

    # ... which grants CDP access ...
    client_headers = {"Authorization": f"Bearer {client_token}"}
    resp = http(f"{url}/json/version", headers=client_headers)
    assert resp.status_code == 200
    assert "Browser" in resp.text

    # ... but not access to the admin-only token API.
    resp = http(f"{url}/api/tokens", headers=client_headers, expected_status=403)
    assert resp.status_code == 403

    # 8. The new token shows up in the token list.
    resp = http(f"{url}/api/tokens", headers=admin_headers)
    assert resp.status_code == 200
    assert any(t["name"] == "my-client" for t in resp.json())

    # 9. Revoke the client token; it must no longer grant access.
    resp = requests.delete(
        f"{url}/api/tokens/{client_token}",
        headers=admin_headers,
        timeout=10,
        verify=not allow_insecure(),
    )
    assert resp.status_code == 200
    assert resp.json()["revoked"] is True

    resp = http(f"{url}/json/version", headers=client_headers, expected_status=401)
    assert resp.status_code == 401
