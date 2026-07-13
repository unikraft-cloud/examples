"""End-to-end test for the ``MySQL`` example.

Mirrors the manual steps from ``mysql/README.md``:

1. ``unikraft build . --output <prefix>/mysql:<tag>``
2. ``unikraft run --metro <metro> -p 3306:3306/tls -m 1G
   -e MYSQL_ROOT_PASSWORD=unikraft --image ...``
3. Connect with a MySQL client (here via ``pymysql``) and run queries.

The README demonstrates:
  ``mysql -h 127.0.0.1 --ssl-mode=DISABLED -u root -punikraft mysql
    <<< "select count(*) from user"``
We replicate that query and add a round-trip table test.
"""

from __future__ import annotations

import pymysql

from _testlib.readiness import retry_until_ready
from _testlib.unikraft import extract_instance_fqdn, extract_instance_name

MYSQL_USER = "root"
MYSQL_PASSWORD = "unikraft"
MYSQL_DATABASE = "mysql"
MYSQL_PORT = 3306


def _connect(port: int):
    """Open a plaintext PyMySQL connection through the socat TLS tunnel.

    Retries while the server initialises: on first boot mysqld builds the
    system tables before it accepts client sessions, and ``wait_instance``
    only proves the unikernel booted.
    """
    return retry_until_ready(
        lambda: pymysql.connect(
            host="127.0.0.1",
            port=port,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            connect_timeout=30,
        ),
        exceptions=pymysql.err.MySQLError,
        description="mysql",
    )


def test_mysql(build_image, run_instance, socat_tunnel, wait_instance):
    """Build, deploy, and exercise a MySQL instance."""
    image = build_image("mysql", "mysql")

    instance = run_instance(
        image,
        publish=["3306:3306/tls"],
        memory="1G",
        env={"MYSQL_ROOT_PASSWORD": MYSQL_PASSWORD},
    )

    host = extract_instance_fqdn(instance)
    assert host, f"could not determine instance FQDN from: {instance!r}"

    # Use a socat TLS tunnel, mirroring the README approach.
    # The platform's /tls port mapping wraps the entire TCP stream in TLS,
    # while MySQL inside speaks plain MySQL protocol.
    tunnel = socat_tunnel(host, MYSQL_PORT, MYSQL_PORT)

    wait_instance(extract_instance_name(instance), "running")
    conn = _connect(tunnel.local_port)
    try:
        cur = conn.cursor()

        # ------------------------------------------------------------------
        # 1. SELECT count(*) FROM user — matches the README demo.
        # ------------------------------------------------------------------
        cur.execute("SELECT count(*) FROM user;")
        row = cur.fetchone()
        assert row is not None
        count = row[0]
        assert isinstance(count, int) and count > 0, (
            f"expected at least one user row, got {count}"
        )

        # ------------------------------------------------------------------
        # 2. Round-trip: CREATE → INSERT → SELECT → DROP.
        # ------------------------------------------------------------------
        cur.execute("CREATE DATABASE IF NOT EXISTS pytest_test;")
        cur.execute("USE pytest_test;")

        cur.execute(
            "CREATE TABLE t ("
            "  id INT AUTO_INCREMENT PRIMARY KEY,"
            "  name VARCHAR(64) NOT NULL"
            ");"
        )
        cur.execute("INSERT INTO t (name) VALUES ('alice'), ('bob');")
        conn.commit()

        cur.execute("SELECT name FROM t ORDER BY id;")
        rows = cur.fetchall()
        assert [r[0] for r in rows] == ["alice", "bob"]

        cur.execute("DROP DATABASE pytest_test;")
        conn.commit()

        cur.close()
    finally:
        conn.close()
