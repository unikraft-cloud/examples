"""End-to-end test for the ``httpserver-flask-redis`` example.

Mirrors the manual steps from ``httpserver-flask-redis/README.md``:

1. Build and deploy the Redis instance (internal, on ``redis-{test_run_id}.internal``).
2. Build and deploy the Flask instance (public, on port 443:8000/tls+http).
3. ``curl https://<instance-url>`` and assert the page-view counter response.

Each request to the Flask app increments a Redis counter. The response
contains "This webpage has been viewed X time(s)".
"""

from __future__ import annotations

import re

from _testlib.unikraft import extract_instance_name, extract_instance_url


def _extract_count(text: str) -> int:
    """Extract the view count from a response like 'viewed 3 time(s)'."""
    match = re.search(r"viewed\s+(\d+)\s+time", text, re.IGNORECASE)
    assert match, f"could not find view count in response: {text!r}"
    return int(match.group(1))


def test_flask_redis_counter(build_image, run_instance, http, test_run_id, wait_instance):
    redis_domain = f"redis-{test_run_id}.internal"

    # 1. Build and deploy internal Redis instance.
    redis_image = build_image("httpserver-flask-redis/redis", "flask-redis-db")

    run_instance(
        redis_image,
        memory="256M",
        domain=redis_domain,
        scale_to_zero={"policy": "idle", "cooldown-time": "1000", "stateful": "true"},
        name=f"redis-{test_run_id}",
    )

    # 2. Build and deploy the Flask app.
    flask_image = build_image("httpserver-flask-redis/flask", "flask-redis-app")

    flask_instance = run_instance(
        flask_image,
        publish=["443:8000/tls+http"],
        memory="512M",
        env={"REDIS_HOST": redis_domain, "REDIS_PORT": "6379"},
        name=f"flask-{test_run_id}",
    )

    url = extract_instance_url(flask_instance)
    assert url, f"could not determine instance URL from: {flask_instance!r}"

    wait_instance(extract_instance_name(flask_instance), "running")

    # 3. First request — counter should be at least 1.
    resp = http(url)
    assert resp.status_code == 200
    count1 = _extract_count(resp.text)
    assert count1 >= 1

    # 4. Second request — counter should have incremented.
    resp2 = http(url)
    assert resp2.status_code == 200
    count2 = _extract_count(resp2.text)
    assert count2 > count1
