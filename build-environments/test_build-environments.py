"""End-to-end test for the ``build-environments`` example.

Mirrors the manual steps from ``build-environments/README.md``:

1. ``unikraft build . --output <prefix>/go-build-env:<tag>``
2. ``unikraft run --metro <metro> --name <tpl> -m 512M --image ...``
   (the instance auto-converts into a template)
3. ``unikraft build rom1/ --output <prefix>/go-rom1:<tag>``
   ``unikraft build rom2/ --output <prefix>/go-rom2:<tag>``
4. ``unikraft run --metro <metro> -p 443:8080/tls+http
   --rom image=<prefix>/go-rom1:<tag>,at=/rom --template <tpl>``
5. ``curl https://<instance-url>`` → "Bye, World!"
6. Repeat with rom2 → "Auf Wiedersehen!"
"""

from __future__ import annotations

import time
import uuid

import pytest

from _testlib.unikraft import extract_instance_url


@pytest.fixture(scope="module")
def _template_and_roms(request, unikraft, repo_root, ukc_image_prefix, test_run_id):
    """Build the base image, wait for template creation, and build ROMs.

    Module-scoped so the expensive template setup is shared across both ROM
    tests in this file.

    Returns a tuple of (template_name, rom1_tag, rom2_tag).
    """
    context = repo_root / "build-environments"
    base_tag = f"{ukc_image_prefix}/go:{test_run_id}"
    template_name = f"go-{test_run_id}"
    rom1_tag = f"{ukc_image_prefix}/go-rom1:{test_run_id}"
    rom2_tag = f"{ukc_image_prefix}/go-rom2:{test_run_id}"

    # Register cleanup in reverse order (LIFO).
    def _cleanup_rom2():
        unikraft.delete_image(rom2_tag)

    def _cleanup_rom1():
        unikraft.delete_image(rom1_tag)

    def _cleanup_template():
        unikraft.run(
            ["instance", "template", "delete", template_name],
            check=False,
        )

    def _cleanup_base():
        unikraft.delete_image(base_tag)

    request.addfinalizer(_cleanup_rom2)
    request.addfinalizer(_cleanup_rom1)
    request.addfinalizer(_cleanup_template)
    request.addfinalizer(_cleanup_base)

    # 1. Build the base image.
    unikraft.build(context, base_tag)

    # 2. Run the base image; it auto-converts into a template.
    unikraft.run_instance(
        base_tag,
        memory="512M",
        name=template_name,
    )

    # 3. Wait for the template to be ready.
    for _ in range(60):
        time.sleep(5)
        proc = unikraft.run(
            ["instance", "template", "ls"],
            check=False,
        )
        if proc.returncode == 0 and template_name in proc.stdout:
            break
    else:
        pytest.fail(f"template {template_name!r} did not become ready within timeout")

    # 4. Build ROM images.
    unikraft.build(context / "rom1", rom1_tag)
    unikraft.build(context / "rom2", rom2_tag)

    return template_name, rom1_tag, rom2_tag


def test_build_environments_rom1(
    _template_and_roms, request, unikraft, test_run_id, http, wait_instance
):
    """Run an instance from the template with ROM1 and verify response."""
    template_name, rom1_tag, _ = _template_and_roms

    instance_name = f"rom1-{test_run_id}"
    request.addfinalizer(lambda: unikraft.delete_instance(instance_name))

    instance = unikraft.run_instance(
        publish=["443:8080/tls+http"],
        name=instance_name,
        template=template_name,
        rom={"image": rom1_tag, "at": "/rom"},
        scale_to_zero={"policy": "on", "cooldown-time": "1000", "stateful": "true"},
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    wait_instance(instance_name, "standby")
    resp = http(url)
    assert resp.status_code == 200
    assert "Bye, World!" in resp.text


def test_build_environments_rom2(
    _template_and_roms, request, unikraft, test_run_id, http, wait_instance
):
    """Run an instance from the template with ROM2 and verify response."""
    template_name, _, rom2_tag = _template_and_roms

    instance_name = f"rom2-{test_run_id}"
    request.addfinalizer(lambda: unikraft.delete_instance(instance_name))

    instance = unikraft.run_instance(
        publish=["443:8080/tls+http"],
        name=instance_name,
        template=template_name,
        rom={"image": rom2_tag, "at": "/rom"},
        scale_to_zero={"policy": "on", "cooldown-time": "1000", "stateful": "true"},
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    wait_instance(instance_name, "standby")
    resp = http(url)
    assert resp.status_code == 200
    assert "Auf Wiedersehen!" in resp.text
