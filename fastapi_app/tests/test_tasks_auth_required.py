from __future__ import annotations


async def test_tasks_requires_auth(client):
    r = await client.get("/tasks/")
    assert r.status_code == 401
