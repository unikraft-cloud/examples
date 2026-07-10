"""Thin wrapper around the `unikraft` CLI binary.

The caller is expected to have already authenticated the CLI (e.g. via
``unikraft login`` or a pre-existing profile). This wrapper does not manage
credentials — it only ensures every invocation targets a specific metro.
"""

from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

log = logging.getLogger(__name__)

UNIKRAFT_BIN = os.environ.get("UNIKRAFT_BIN", "unikraft")


def _as_tuple(value: str | Sequence[str] | None) -> tuple[str, ...]:
    """Accept a single value or a sequence for repeatable flags."""
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    return tuple(value)


def _as_spec(value: str | Mapping[str, Any]) -> str:
    """Render a mapping as a comma-separated ``key=value`` spec string.

    Accepts a ready-made string and returns it unchanged, so callers can
    mix the two forms freely.
    """
    if isinstance(value, Mapping):
        return ",".join(f"{k}={v}" for k, v in value.items())
    return value


def _as_spec_tuple(
    value: str | Mapping[str, Any] | Sequence[str | Mapping[str, Any]] | None,
) -> tuple[str, ...]:
    """Like ``_as_tuple`` but each element may also be a mapping."""
    if value is None:
        return ()
    if isinstance(value, (str, Mapping)):
        return (_as_spec(value),)
    return tuple(_as_spec(v) for v in value)


class UnikraftError(RuntimeError):
    """Raised when a `unikraft` CLI invocation fails."""


def _resolve_bin() -> str:
    path = shutil.which(UNIKRAFT_BIN)
    if path is None:
        raise UnikraftError(
            f"`{UNIKRAFT_BIN}` binary not found on PATH. "
            "Install the Unikraft CLI: https://unikraft.com/docs/cli/unikraft"
        )
    return path


@dataclass
class UnikraftCLI:
    """Invokes the `unikraft` CLI against a specific metro.

    Authentication is expected to come from the user's existing CLI profile
    (as configured by ``unikraft login``). ``metro`` is passed explicitly on
    every command that accepts it.
    """

    metro: str

    def run(
        self,
        args: Sequence[str],
        *,
        cwd: str | os.PathLike[str] | None = None,
        check: bool = True,
        capture_output: bool = True,
        timeout: float | None = 600,
    ) -> subprocess.CompletedProcess[str]:
        bin_path = _resolve_bin()
        cmd = [bin_path, *args]
        log.debug("exec: %s (cwd=%s)", " ".join(cmd), cwd)

        proc = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            check=False,
            capture_output=capture_output,
            text=True,
            timeout=timeout,
        )

        if proc.stdout:
            log.debug("stdout: %s", proc.stdout.strip())
        if proc.stderr:
            log.debug("stderr: %s", proc.stderr.strip())
        if check and proc.returncode != 0:
            raise UnikraftError(
                f"`unikraft {' '.join(args)}` exited with {proc.returncode}\n"
                f"stdout: {proc.stdout}\n"
                f"stderr: {proc.stderr}"
            )
        
        return proc

    # ------------------------------------------------------------------
    # High-level helpers
    # ------------------------------------------------------------------

    def build(
        self,
        context: str | os.PathLike[str],
        output: str,
        *,
        extra_args: Sequence[str] = (),
    ) -> None:
        """Build an image from ``context`` and publish/tag it as ``output``.

        ``output`` is typically ``<org>/<name>:<tag>`` as shown in example
        READMEs, e.g. ``my-org/nginx:test``.
        """
        log.info(
            "building image from context %s with output tag %s", 
            context, 
            output
        )
        self.run(["build", str(context), "--output", output, *extra_args])

    def run_instance(
        self,
        image: str | None = None,
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
        """Start an instance and return its parsed JSON description.

        Parameters mirror the ``unikraft run`` flags shown in the example
        READMEs, so tests can express exactly what the docs tell users to
        run without falling back to ``extra_args``:

        * ``publish`` – ``-p`` port mappings, e.g. ``["443:8080/tls+http"]``.
        * ``memory`` – ``-m``, e.g. ``"256M"``.
        * ``name`` – ``-n``; tests usually let the fixture generate one.
        * ``metro`` – per-call override of the CLI's default metro.
        * ``scale_to_zero`` – ``--scale-to-zero`` spec; either a verbatim
          string (``"policy=on,cooldown-time=1000,stateful=true"``) or a
          mapping (``{"policy": "on", "cooldown-time": "1000", ...}``).
        * ``template`` – ``--template`` name.
        * ``env`` – ``--env`` entries; either ``"KEY=VALUE"`` strings or a
          mapping (rendered in iteration order).
        * ``domain`` – one or more ``--domain`` values.
        * ``volume`` – one or more ``--volume`` mounts, ``"name:/path"``.
        * ``rom`` – one or more ``--rom`` specs; each may be a verbatim
          string (``"image=...,at=/rom"``) or a mapping
          (``{"image": "...", "at": "/rom"}``).
        * ``vcpus`` – ``--vcpus``.
        * ``command`` – the command override placed after ``--``. A string
          is passed as the single quoted argument shown in READMEs
          (``-- "/usr/local/bin/python /src/server.py"``); a sequence is
          passed as separate arguments. Always emitted last.
        * ``extra_args`` – escape hatch for flags not modelled above.
        """
        args: list[str] = ["run", "--metro", metro or self.metro,
                           "--output", "json"]
        if scale_to_zero:
            args += ["--scale-to-zero", _as_spec(scale_to_zero)]
        for v in _as_tuple(volume):
            args += ["--volume", v]
        for p in publish:
            args += ["-p", p]
        if memory:
            args += ["-m", memory]
        if vcpus is not None:
            args += ["--vcpus", str(vcpus)]
        if name:
            args += ["-n", name]
        if image:
            args += ["--image", image]
        for d in _as_tuple(domain):
            args += ["--domain", d]
        if isinstance(env, Mapping):
            env = [f"{k}={v}" for k, v in env.items()]
        for e in env:
            args += ["--env", e]
        for r in _as_spec_tuple(rom):
            args += ["--rom", r]
        if template:
            args += ["--template", template]
        args += list(extra_args)
        # `--` terminates option parsing; everything after it is the
        # instance command, so it must come last — after extra_args too.
        if command is not None:
            args.append("--")
            if isinstance(command, str):
                args.append(command)
            else:
                args.extend(command)

        log.info(
            "running instance with image %s (publish=%s, memory=%s, name=%s)",
            image,
            publish,
            memory,
            name,
        )
        proc = self.run(args)

        return _parse_json(proc.stdout)

    def get_instance(self, target: str) -> dict[str, Any]:
        proc = self.run(
            [
                "instances",
                "get",
                target,
                "--metro",
                self.metro,
                "--output",
                "json",
            ]
        )

        return _parse_json(proc.stdout)

    def wait_instance(
        self, target: str, state: str, *, timeout: float | None = 150
    ) -> dict[str, Any]:
        """Wait until ``target`` reaches the given ``state``.

        Wraps ``unikraft instances wait <target> --until state==<state>``.
        Returns the parsed JSON description of the instance once it reaches
        the desired state.
        """
        proc = self.run(
            [
                "instances",
                "wait",
                target,
                "--until",
                f"state=={state}",
                "--output",
                "json",
            ],
            timeout=timeout,
        )
        return _parse_json(proc.stdout)

    def delete_instance(self, target: str) -> None:
        try:
            proc =self.run(["instances", "delete", target], check=False)
            if proc.returncode != 0:
                log.error(
                    "failed to delete instance %s (exit=%d)\n"
                    "stdout: %s\nstderr: %s",
                    target,
                    proc.returncode,
                    proc.stdout,
                    proc.stderr,
                )
            else:
                log.info("deleted instance %s", target)
        except Exception:
            log.exception("error deleting instance %s", target)

    def delete_image(self, target: str) -> None:
        """Best-effort removal of an image by tag. Never raises.

        Must be called *after* every instance that references the image has
        been deleted — the registry rejects removal of in-use images.
        """
        try:
            proc = self.run(["images", "delete", target], check=False)
            if proc.returncode != 0:
                log.error(
                    "failed to delete image %s (exit=%d)\n"
                    "stdout: %s\nstderr: %s",
                    target,
                    proc.returncode,
                    proc.stdout,
                    proc.stderr,
                )
            else:
                log.info("deleted image %s", target)
        except Exception:
            log.exception("error deleting image %s", target)


def _parse_json(raw: str) -> dict[str, Any]:
    """Parse CLI JSON output.

    The CLI may emit either a single object or a list (for list commands).
    For single-instance commands we unwrap a one-element list.
    """
    raw = raw.strip()
    if not raw:
        raise UnikraftError("empty JSON response from unikraft CLI")
    
    data = json.loads(raw)
    if isinstance(data, list):
        if len(data) != 1:
            # TODO: decide on behaviour for list responses with != 1 entries.
            raise UnikraftError(
                f"expected exactly one item in JSON response, got {len(data)}"
            )
        return data[0]
    
    if isinstance(data, dict):
        return data
    
    raise UnikraftError(f"unexpected JSON payload type: {type(data).__name__}")


def extract_instance_url(instance: dict[str, Any]) -> str | None:
    """Best-effort extraction of a public URL for an instance.

    The `unikraft run` JSON output shape is not part of a documented stable
    contract, so we probe a few known field names. Returns ``None`` if no URL
    can be found.
    """
    # TODO: confirm the exact JSON shape emitted by `unikraft run --output json`
    # and tighten this helper once the schema is stable.
    for key in ("url", "fqdn"):
        value = instance.get(key)
        if isinstance(value, str) and value:
            return value if value.startswith("http") else f"https://{value}"

    service = instance.get("service")
    if isinstance(service, dict):
        domains = service.get("domains")
        if isinstance(domains, list):
            for domain in domains:
                if isinstance(domain, dict):
                    fqdn = domain.get("fqdn")
                    if isinstance(fqdn, str) and fqdn:
                        return f"https://{fqdn}"
    return None


def extract_instance_name(instance: dict[str, Any]) -> str:
    name = instance.get("name") or instance.get("uuid")
    if not isinstance(name, str) or not name:
        raise UnikraftError(
            "could not determine instance name/uuid from CLI output"
        )
    return name


def extract_instance_fqdn(instance: dict[str, Any]) -> str | None:
    """Best-effort extraction of the bare FQDN (no scheme) for an instance.

    Useful for non-HTTP clients (databases, caches, etc.) that need a
    hostname to connect to over TLS.
    """
    from urllib.parse import urlparse

    url = extract_instance_url(instance)
    if url is None:
        return None
    parsed = urlparse(url)
    return parsed.hostname
