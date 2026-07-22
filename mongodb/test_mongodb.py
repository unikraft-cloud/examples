"""End-to-end test for the ``mongodb`` example.

Mirrors the manual steps from ``mongodb/README.md``:

1. ``unikraft build . --output <prefix>/mongodb:<tag>``
2. ``unikraft run --metro <metro> -p 27017:27017/tls -m 1G --image ...``
3. Connect with ``mongosh`` (here via ``pymongo``) and run operations.

The README demonstrates connecting via:
  ``mongosh "mongodb://<fqdn>:27017/?tls=true"``
and shows MongoDB 6.0.13 in the output.  We replicate the connection
and exercise basic CRUD operations.
"""

from __future__ import annotations

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from _testlib.readiness import retry_until_ready
from _testlib.unikraft import extract_instance_fqdn, extract_instance_name

MONGO_PORT = 27017


def _connect(host: str) -> MongoClient:
    """Open a pymongo client to the instance over TLS, ready to use.

    MongoClient connects lazily, so constructing it proves nothing; a ping is
    the first call that actually performs server selection, and is therefore
    what we retry while mongod finishes starting.
    """
    uri = f"mongodb://{host}:{MONGO_PORT}/?tls=true&directConnection=true"
    client = MongoClient(
        uri,
        serverSelectionTimeoutMS=30000,
        connectTimeoutMS=30000,
    )

    retry_until_ready(
        lambda: client.admin.command("ping"),
        exceptions=PyMongoError,
        description="mongodb",
    )

    return client


def test_mongodb(build_image, run_instance, wait_instance):
    """Build, deploy, and exercise a MongoDB instance."""
    image = build_image("mongodb", "mongodb")

    instance = run_instance(
        image,
        publish=["27017:27017/tls"],
        memory="1G",
    )

    host = extract_instance_fqdn(instance)
    assert host, f"could not determine instance FQDN from: {instance!r}"

    wait_instance(extract_instance_name(instance), "running")
    client = _connect(host)
    try:
        # ------------------------------------------------------------------
        # 1. ping — baseline connectivity (like 'SELECT 1' for SQL DBs).
        # ------------------------------------------------------------------
        result = client.admin.command("ping")
        assert result.get("ok") == 1.0

        # ------------------------------------------------------------------
        # 2. Server info — verify we're talking to MongoDB.
        # ------------------------------------------------------------------
        info = client.server_info()
        assert "version" in info

        # ------------------------------------------------------------------
        # 3. CRUD round-trip: insert → find → update → delete.
        # ------------------------------------------------------------------
        db = client["pytest_test"]
        collection = db["items"]

        # Clean slate.
        collection.drop()

        # Insert documents.
        collection.insert_many(
            [
                {"name": "alice", "score": 10},
                {"name": "bob", "score": 20},
            ]
        )
        assert collection.count_documents({}) == 2

        # Find.
        alice = collection.find_one({"name": "alice"})
        assert alice is not None
        assert alice["score"] == 10

        # Update.
        collection.update_one({"name": "alice"}, {"$set": {"score": 15}})
        alice = collection.find_one({"name": "alice"})
        assert alice["score"] == 15

        # Sorted query.
        names = [doc["name"] for doc in collection.find().sort("name", 1)]
        assert names == ["alice", "bob"]

        # Delete one document and verify count.
        collection.delete_one({"name": "bob"})
        assert collection.count_documents({}) == 1

        # Clean up.
        collection.drop()
        client.drop_database("pytest_test")
    finally:
        client.close()
