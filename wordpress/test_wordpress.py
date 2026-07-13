"""End-to-end test for the ``wordpress`` example.

Mirrors the manual steps from ``wordpress/README.md``:

1. Create volumes for WordPress and MariaDB data.
2. Build and deploy the MariaDB instance (internal, on
   ``wordpress-mariadb.internal``).
3. Build and deploy the WordPress instance (public, on
   port 443:8080/tls+http).
4. ``curl https://<instance-url>`` and assert WordPress is served.
"""

from __future__ import annotations

import logging

from _testlib.unikraft import extract_instance_name, extract_instance_url

log = logging.getLogger(__name__)

MARIADB_ROOT_PASSWORD = "unikraft"


def test_wordpress_serves_page(build_image, run_instance, http, unikraft, request, test_run_id, wait_instance):
    wp_volume = f"wordpress-wp-data-{test_run_id}"
    db_volume = f"wordpress-db-data-{test_run_id}"

    def _cleanup_volumes():
        for vol in (wp_volume, db_volume):
            try:
                unikraft.run(["volume", "delete", vol], check=False)
                log.info("deleted volume %s", vol)
            except Exception:
                log.exception("error deleting volume %s", vol)

    request.addfinalizer(_cleanup_volumes)

    # 1. Create volumes for MariaDB and WordPress.
    for vol in (wp_volume, db_volume):
        unikraft.run([
            "volume", "create",
            "--metro", unikraft.metro,
            f"--name={vol}",
            "--size=512M",
        ])

    # 2. Build and deploy the MariaDB instance.
    mariadb_image = build_image("wordpress/mariadb", "wordpress-mariadb")

    mariadb_domain = f"{test_run_id}-mariadb.internal"

    run_instance(
        mariadb_image,
        memory="1G",
        domain=mariadb_domain,
        volume=f"{db_volume}:/var/lib/mysql",
        env={"MARIADB_ROOT_PASSWORD": MARIADB_ROOT_PASSWORD},
        name=f"mariadb-{test_run_id}",
    )

    # 3. Build and deploy the WordPress instance.
    wp_image = build_image("wordpress/wordpress", "wordpress-app")

    wp_instance = run_instance(
        wp_image,
        publish=["443:8080/tls+http"],
        memory="2G",
        volume=f"{wp_volume}:/var/www/html",
        name=f"wordpress-{test_run_id}",
        env={"WORDPRESS_DB_HOST": mariadb_domain},
    )

    url = extract_instance_url(wp_instance)
    assert url, f"could not determine instance URL from: {wp_instance!r}"

    wait_instance(extract_instance_name(wp_instance), "running")

    # 4. Verify WordPress is served (install page or homepage).
    resp = http(url)
    assert resp.status_code == 200
    assert "WordPress" in resp.text or "wp-" in resp.text
