# Examples test suite

End-to-end tests for the examples in this repository. Tests build an example,
deploy it to Unikraft Cloud via the `unikraft` CLI, exercise it over HTTP,
and then tear the instance down.

## Prerequisites

* Python 3.10+
* The [`unikraft`](https://unikraft.com/docs/cli/unikraft) CLI on `PATH`
  (override with `UNIKRAFT_BIN`), already authenticated via
  `unikraft login` (the tests rely on your existing CLI profile).
* A working container runtime (Docker or compatible) — required by
  `unikraft build`.
* System packages: `socat`, `ssh`, `lftp` — required by tests that exercise
  non-HTTP services (SSH, FTP) behind TLS port mappings.

## Setup

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment variables

| Variable            | Required | Description                                                   |
| ------------------- | -------- | ------------------------------------------------------------- |
| `UKC_METRO`         | yes      | Metro to deploy into (e.g. `fra`, `sfo`, `was`).              |
| `UKC_IMAGE_PREFIX`  | yes      | Image repository prefix, typically your org name (`my-org`).  |
| `UKC_ARCH`          | no       | Architecture to build for (`x86_64`, `arm64`), passed to `unikraft build --arch`. Unset builds the target(s) declared in each Kraftfile. |
| `UKC_ALLOW_INSECURE`| no       | If truthy (`1`/`true`), disable TLS verification for HTTP calls (for self-signed certs). |
| `UNIKRAFT_BIN`      | no       | Path to the `unikraft` binary (default: `unikraft` on `PATH`).|

Authentication is handled by your existing `unikraft` CLI profile — run
`unikraft login` once before running the tests. Tests that require one of the
variables above will be **skipped** if it is unset.

## Running

```bash
# Run everything
pytest

# Run only the nginx test
pytest nginx

# Verbose + live logs
pytest -s
```

## Layout

Each example owns its own test file, so related changes stay together. A
single `pytest` invocation at the repo root discovers them all:

```
conftest.py            # shared fixtures: CLI, build_image, run_instance, http
pytest.ini             # pytest config (uses importlib import mode)
_testlib/              # shared helpers (not collected as tests)
├── unikraft.py        # thin wrapper around the `unikraft` CLI binary
└── http_client.py     # HTTP GET helper with retries
<example>/             # e.g. nginx/, postgres/, …
├── Dockerfile
├── Kraftfile
└── test_<example>.py  # end-to-end test for this example
```

### Fixtures

* `unikraft` — session-scoped `UnikraftCLI` wrapper.
* `build_image(example_dir, image_name)` — builds an example directory,
  returns the full image tag.
* `run_instance(image, **kwargs)` — launches an instance; automatically
  removed during teardown.
* `http` — `requests.get`-style helper with retries/backoff.
* `ukc_metro`, `ukc_image_prefix`, `ukc_arch`, `test_run_id`, `repo_root`.

## Adding a new test

1. Create `<example-name>/test_<example-name>.py` next to the example's
   `Dockerfile` / `Kraftfile`.
2. Use `build_image` and `run_instance` to deploy, then assert behaviour via
   `http` (or any other client).
3. Instances are torn down automatically — no manual cleanup needed.
