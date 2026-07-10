"""End-to-end test for the ``visual-studio-code-server`` example.

Mirrors the manual steps from ``visual-studio-code-server/README.md`` and
the existing CI workflow (example-visual-studio-code-server-stable.yaml):

1. Create a volume for workspace persistence.
2. ``unikraft build . --output <prefix>/visual-studio-code-server:<tag>``
3. ``unikraft run --metro <metro> -p 443:8443/tls+http -m 2G
   --volume <vol>:/workspace -e PASSWORD=unikraft ... --image ...``
4. ``curl https://<instance-url>`` → HTTP 200 (Code Server login page).
"""

from __future__ import annotations

import logging

from _testlib.unikraft import extract_instance_name, extract_instance_url

log = logging.getLogger(__name__)


def test_visual_studio_code_server(
    request, build_image, run_instance, unikraft, http, wait_instance, test_run_id
):
    """Build, deploy, and verify the VS Code Server login page loads."""
    # Create a volume for workspace persistence, matching the old workflow.
    vol_name = f"code-{test_run_id}"
    unikraft.run([
        "volume", "create",
        "--set", f"name={vol_name}",
        "--set", "size=1G",
        "--set", f"metro={unikraft.metro}",
    ])

    # Register volume cleanup *before* run_instance so pytest's LIFO
    # finalizer ordering deletes the instance first, then the volume.
    def _delete_volume():
        try:
            unikraft.run(["volume", "delete", vol_name], check=False)
        except Exception:
            log.warning("failed to delete volume %s", vol_name)

    request.addfinalizer(_delete_volume)

    image = build_image(
        "visual-studio-code-server", "visual-studio-code-server"
    )

    instance = run_instance(
        image,
        publish=["443:8443/tls+http"],
        memory="2G",
        volume=f"{vol_name}:/workspace",
        env={
            "PGUID": "0",
            "PGID": "0",
            "PASSWORD": "unikraft",
            "SUDO_PASSWORD": "unikraft",
            "DEFAULT_WORKSPACE": "/workspace",
        },
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    wait_instance(extract_instance_name(instance), "running")

    resp = http(url)
    assert resp.status_code == 200
