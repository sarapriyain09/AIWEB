from __future__ import annotations


async def test_auth_and_tasks_flow_sqlite(client, random_email):
    # Register
    r = await client.post("/auth/register", json={"email": random_email, "password": "Password123"})
    assert r.status_code == 201
    token = r.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # Create task
    r = await client.post("/tasks/", json={"title": "t1", "description": "d1"}, headers=headers)
    assert r.status_code == 201
    task_id = r.json()["id"]

    # List tasks
    r = await client.get("/tasks/", headers=headers)
    assert r.status_code == 200
    assert any(t["id"] == task_id for t in r.json())

    # Update task
    r = await client.patch(f"/tasks/{task_id}", json={"is_done": True}, headers=headers)
    assert r.status_code == 200
    assert r.json()["is_done"] is True

    # Delete task
    r = await client.delete(f"/tasks/{task_id}", headers=headers)
    assert r.status_code == 204

    # Ensure deleted
    r = await client.get(f"/tasks/{task_id}", headers=headers)
    assert r.status_code == 404
