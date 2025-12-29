from __future__ import annotations


async def test_register_validation(client):
    r = await client.post("/auth/register", json={"email": "not-an-email", "password": "123"})
    assert r.status_code == 422


async def test_login_requires_payload(client):
    r = await client.post("/auth/login", json={})
    assert r.status_code == 422
