"""End-to-end test for the ``nginx-flask-mongo`` example.

Mirrors the manual steps from ``nginx-flask-mongo/README.md``:

1. Create a volume for MongoDB data persistence.
2. Build and deploy MongoDB (internal, on ``mongo-{test_run_id}.internal``).
3. Build and deploy Flask backend (internal, on ``backend.internal``).
4. Build and deploy Nginx reverse proxy (public, on port 443:80/tls+http).
5. ``curl https://<instance-url>`` and assert "Hello from the MongoDB client!".
"""

from __future__ import annotations

import logging

from _testlib.unikraft import extract_instance_name, extract_instance_url

log = logging.getLogger(__name__)


def test_nginx_flask_mongo(build_image, run_instance, http, unikraft, request, test_run_id, wait_instance):
    volume_name = f"nginx-flask-mongo-data-{test_run_id}"

    def _cleanup_volume():
        try:
            unikraft.run(["volume", "delete", volume_name], check=False)
            log.info("deleted volume %s", volume_name)
        except Exception:
            log.exception("error deleting volume %s", volume_name)

    request.addfinalizer(_cleanup_volume)

    # 1. Create the MongoDB volume.
    unikraft.run([
        "volume", "create",
        "--metro", unikraft.metro,
        f"--name={volume_name}",
        "--size=1G",
    ])

    mongo_domain = f"mongo-{test_run_id}.internal"

    # 2. Build and deploy MongoDB.
    mongo_image = build_image("nginx-flask-mongo/mongo", "nfm-mongo")

    run_instance(
        mongo_image,
        memory="1024M",
        domain=mongo_domain,
        scale_to_zero={"policy": "idle", "cooldown-time": "1000", "stateful": "true"},
        volume=f"{volume_name}:/data/db",
    )

    # 3. Build and deploy Flask backend.
    backend_domain = "backend.internal"
    flask_image = build_image("nginx-flask-mongo/flask", "nfm-flask")

    run_instance(
        flask_image,
        memory="1024M",
        domain=backend_domain,
        env={"FLASK_SERVER_PORT": "9091", "MONGO_SERVER_URL": f"{mongo_domain}:27017"},
    )

    # 4. Build and deploy Nginx reverse proxy.
    # BACKEND_HOST tells NGINX which internal domain to proxy to.
    nginx_image = build_image("nginx-flask-mongo/nginx", "nfm-nginx")

    nginx_instance = run_instance(
        nginx_image,
        publish=["443:80/tls+http"],
        memory="512M",
        env={"BACKEND_HOST": backend_domain},
    )

    url = extract_instance_url(nginx_instance)
    assert url, f"could not determine instance URL from: {nginx_instance!r}"

    wait_instance(extract_instance_name(nginx_instance), "running")

    # 5. Verify the response from the full stack.
    resp = http(url)
    assert resp.status_code == 200
    assert "Hello from the MongoDB client!" in resp.text
