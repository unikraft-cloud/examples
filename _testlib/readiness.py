"""Readiness helper for services that are still warming up.

``wait_instance(..., "running")`` reports the Unikraft Cloud *instance*
lifecycle state — the unikernel booted and its entrypoint started. It says
nothing about whether the service inside has finished initialising, and
because unikernels boot in milliseconds that second gap is routinely the
larger of the two.

Databases make this especially visible: they accept TCP connections well
before they are ready to serve. PostgreSQL answers with ``FATAL: the database
system is starting up`` while ``initdb`` runs, and a client-side
``connect_timeout`` does not help — the connection itself *succeeds*, the
server simply rejects the session.

:func:`retry_until_ready` closes that gap for connection-oriented clients,
mirroring the retry behaviour :mod:`_testlib.http_client` already provides for
HTTP endpoints.
"""

from __future__ import annotations

import logging
import time
from typing import Callable, TypeVar

log = logging.getLogger(__name__)

T = TypeVar("T")

DEFAULT_TIMEOUT = 120.0
DEFAULT_BACKOFF = 2.0


def retry_until_ready(
    fn: Callable[[], T],
    *,
    exceptions: type[BaseException] | tuple[type[BaseException], ...],
    timeout: float = DEFAULT_TIMEOUT,
    backoff: float = DEFAULT_BACKOFF,
    description: str = "service",
) -> T:
    """Call ``fn`` until it succeeds, returning its result.

    The budget is wall-clock (``timeout`` seconds in total), deliberately not a
    retry count: these clients already carry their own multi-second connect
    timeouts, so a fixed number of attempts would multiply into a worst case of
    many minutes. A deadline bounds the total regardless of how long any single
    attempt blocks.

    Only ``exceptions`` are retried; anything else propagates immediately, so a
    genuine bug is never hidden behind a warm-up loop. If the budget expires,
    the last failure is re-raised with its original traceback.

    Wrap whichever call actually performs I/O:

    * Eager clients (``psycopg2``, ``pymysql``) connect in the constructor, so
      wrap the constructor and keep what it returns::

          conn = retry_until_ready(
              lambda: psycopg2.connect(...),
              exceptions=psycopg2.OperationalError,
              description="postgres",
          )

    * Lazy clients (``redis``, ``pymongo``, ``pymemcache``) do no I/O until
      first use, so the constructor alone proves nothing. Build the client once
      and wrap a cheap readiness probe instead::

          client = redis.Redis(...)
          retry_until_ready(
              client.ping,
              exceptions=redis.ConnectionError,
              description="redis",
          )
    """
    deadline = time.monotonic() + timeout
    attempt = 0

    while True:
        attempt += 1
        try:
            return fn()
        except exceptions as exc:
            remaining = deadline - time.monotonic()
            log.warning(
                "%s not ready (attempt %d, %.0fs of budget left): %s",
                description,
                attempt,
                max(remaining, 0.0),
                exc,
            )
            if remaining <= backoff:
                raise
            time.sleep(backoff)
