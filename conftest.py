"""Top-level pytest fixtures shared by all example test suites.

These fixtures wrap the ``unikraft`` CLI binary and provide reusable building
blocks for end-to-end tests that deploy an example to Unikraft Cloud and
exercise it over HTTP.

Authentication is expected to come from the caller's existing Unikraft CLI
profile (set up via ``unikraft login``). The tests do not read or manage API
tokens themselves.

Required environment variables:

* ``UKC_METRO`` – Unikraft Cloud metro to deploy into, e.g. ``fra``.
* ``UKC_IMAGE_PREFIX`` – Prefix used when tagging built images, typically the
  user's organisation name (e.g. ``my-org``). Required for tests that build an
  image.
"""

from __future__ import annotations

import logging
import os
import time
import uuid
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Any

import pytest

from _testlib.http_client import http_get, http_post
from _testlib.socat import SocatTunnel
from _testlib.unikraft import (
    UnikraftCLI,
    extract_instance_name,
    extract_instance_url,
)

log = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent


# ---------------------------------------------------------------------------
# Environment / configuration
# ---------------------------------------------------------------------------


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        pytest.skip(f"{name} is not set in the environment")
    return value


@pytest.fixture(scope="session")
def ukc_metro() -> str:
    return _require_env("UKC_METRO")


@pytest.fixture(scope="session")
def ukc_image_prefix() -> str:
    """Image repository prefix (typically the user's org name).

    E.g. if set to ``my-org``, built images will be tagged
    ``my-org/<example>:<tag>``.
    """
    return _require_env("UKC_IMAGE_PREFIX")


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture(scope="session")
def test_run_id() -> str:
    """Identifier unique to this pytest session, taken from ``UKC_TEST_ID``.

    Set ``UKC_TEST_ID`` to the CI run ID (e.g. ``${{ github.run_id }}``) so
    that resources can be correlated and cleaned up after the run.
    """
    return _require_env("UKC_TEST_ID")


# ---------------------------------------------------------------------------
# Unikraft CLI
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def unikraft(ukc_metro: str) -> UnikraftCLI:
    """Session-scoped Unikraft CLI wrapper."""
    return UnikraftCLI(metro=ukc_metro)


# ---------------------------------------------------------------------------
# Image build fixture
# ---------------------------------------------------------------------------


BuildImage = Callable[[str, str], str]


@pytest.fixture
def build_image(
    request: pytest.FixtureRequest,
    unikraft: UnikraftCLI,
    repo_root: Path,
    ukc_image_prefix: str,
    test_run_id: str,
) -> BuildImage:
    """Factory fixture that builds an example directory into an image.

    Usage::

        def test_foo(build_image):
            image = build_image("nginx", "nginx")

    ``example_dir`` is resolved relative to the repository root. ``image_name``
    is the short image name (without prefix/tag); the final tag is
    ``<UKC_IMAGE_PREFIX>/<image_name>:test-<run-id>``.

    A finalizer is registered to delete the image after the test finishes.
    Pytest runs finalizers in LIFO order across fixtures, so any
    ``run_instance`` teardowns (registered later in the test) execute
    *before* this image-delete, ensuring the image is no longer in use.
    """

    def _build(example_dir: str, image_name: str) -> str:
        context = repo_root / example_dir
        assert context.is_dir(), f"example directory not found: {context}"

        tag = f"{ukc_image_prefix}/{image_name}:{test_run_id}"

        # Register the image-delete finalizer *before* invoking the build
        # so a partial build is still cleaned up.
        request.addfinalizer(lambda: unikraft.delete_image(tag))

        unikraft.build(context, tag)

        return tag

    return _build


# ---------------------------------------------------------------------------
# Instance lifecycle fixture
# ---------------------------------------------------------------------------


RunInstance = Callable[..., dict[str, Any]]


@pytest.fixture
def run_instance(
    request: pytest.FixtureRequest,
    unikraft: UnikraftCLI,
    test_run_id: str,
) -> RunInstance:
    """Factory fixture that launches instances with guaranteed teardown.

    Each call creates a new instance. A cleanup finalizer is registered
    **before** invoking the CLI, so the instance is deleted even if the
    ``unikraft run`` command or subsequent JSON parsing fails part-way
    through. Finalizers registered via :meth:`request.addfinalizer` are
    executed by pytest unconditionally after the test completes, whether it
    passed, failed, or errored.

    Parameters passed through to the CLI (see
    :meth:`_testlib.unikraft.UnikraftCLI.run_instance` for full details):

    * ``image`` (positional) – image tag to run.
    * ``publish`` – iterable of ``-p`` port mappings, e.g.
      ``["443:8080/tls+http"]``. Defaults to none.
    * ``memory`` – memory allocation (``-m``), e.g. ``"256M"``. Defaults to
      the CLI default.
    * ``name`` – explicit instance name. If omitted, a unique name is
      generated so parallel runs don't collide.
    * ``metro`` – per-call metro override.
    * ``scale_to_zero`` – ``--scale-to-zero`` spec string, e.g.
      ``"policy=on,cooldown-time=1000"``.
    * ``template`` – ``--template`` name.
    * ``env`` – ``--env`` entries (``"K=V"`` strings or a mapping).
    * ``domain`` / ``volume`` / ``rom`` – single value or sequence for the
      corresponding repeatable flags.
    * ``vcpus`` – ``--vcpus``.
    * ``command`` – instance command placed after ``--`` (string or
      sequence of arguments).
    * ``extra_args`` – extra positional CLI flags for escape-hatch needs.
    """

    def _run(
        image: str,
        *,
        publish: Sequence[str] = (),
        memory: str | None = None,
        name: str | None = None,
        metro: str | None = None,
        scale_to_zero: str | Mapping[str, Any] | None = None,
        template: str | None = None,
        env: Sequence[str] | Mapping[str, Any] = (),
        domain: str | Sequence[str] | None = None,
        volume: str | Sequence[str] | None = None,
        rom: str | Mapping[str, Any] | Sequence[str | Mapping[str, Any]] | None = None,
        vcpus: int | str | None = None,
        command: str | Sequence[str] | None = None,
        extra_args: Sequence[str] = (),
    ) -> dict[str, Any]:
        instance_name = name or f"{test_run_id}"

        # Identifier used by the finalizer. Seeded with the name we asked
        # the CLI to use so teardown still works if `unikraft run` raises
        # before returning a parsed response. Replaced below with the
        # CLI-reported name/uuid once we have it.
        cleanup_target = instance_name

        def _cleanup() -> None:
            log.info("tearing down instance: %s", cleanup_target)
            unikraft.delete_instance(cleanup_target)

        # Register the finalizer before invoking the CLI so the instance is
        # torn down even if `unikraft run` fails mid-flight after having
        # created the instance on the cloud side.
        request.addfinalizer(_cleanup)

        instance = unikraft.run_instance(
            image,
            publish=publish,
            memory=memory,
            name=instance_name,
            metro=metro,
            scale_to_zero=scale_to_zero,
            template=template,
            env=env,
            domain=domain,
            volume=volume,
            rom=rom,
            vcpus=vcpus,
            command=command,
            extra_args=extra_args,
        )

        # Prefer the CLI-reported identifier in case it diverges from the
        # name we requested. `delete_instance` accepts either name or uuid.
        for key in ("name", "uuid"):
            value = instance.get(key)
            if isinstance(value, str) and value:
                cleanup_target = value
                break

        return instance

    return _run


# ---------------------------------------------------------------------------
# Instance wait fixture
# ---------------------------------------------------------------------------


WaitInstance = Callable[[str, str], dict[str, Any]]


@pytest.fixture
def wait_instance(unikraft: UnikraftCLI) -> WaitInstance:
    """Wait until a named instance reaches the given state.

    Usage::

        def test_foo(run_instance, wait_instance):
            instance = run_instance(image, ...)
            wait_instance(extract_instance_name(instance), "running")
    """

    def _wait(target: str, state: str) -> dict[str, Any]:
        return unikraft.wait_instance(target, state)

    return _wait


# ---------------------------------------------------------------------------
# HTTP helper
# ---------------------------------------------------------------------------


@pytest.fixture
def http():
    """Expose the shared HTTP GET helper as a fixture for convenience."""
    return http_get


@pytest.fixture(name="http_post")
def http_post_fixture():
    """Expose the shared HTTP POST helper as a fixture for convenience."""
    return http_post


# ---------------------------------------------------------------------------
# TLS tunnel (socat) helper
# ---------------------------------------------------------------------------


SocatTunnelFactory = Callable[[str, int, int], SocatTunnel]


@pytest.fixture
def socat_tunnel(request: pytest.FixtureRequest) -> SocatTunnelFactory:
    """Factory fixture that creates socat TLS tunnels with guaranteed teardown.

    ``local_port`` is the TCP port socat will listen on locally.

    Usage::

        def test_mydb(socat_tunnel, ...):
            tunnel = socat_tunnel(host, 3306, 3306)
            conn = my_connect("127.0.0.1", tunnel.local_port)
    """

    def _create(host: str, port: int, local_port: int) -> SocatTunnel:
        tunnel = SocatTunnel(host, port, local_port)
        tunnel.open()
        request.addfinalizer(tunnel.close)
        return tunnel

    return _create


# Re-export for callers that import from conftest.
__all__ = [
    "build_image",
    "extract_instance_url",
    "http",
    "http_post",
    "run_instance",
    "socat_tunnel",
    "unikraft",
    "wait_instance",
]
